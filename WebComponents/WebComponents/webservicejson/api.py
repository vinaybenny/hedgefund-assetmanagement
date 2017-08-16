from django.contrib.auth.models import User
from django.db.models import Max
from WebComponents.webservicejson.models import SimulationModel, SimulationResult
from tastypie import fields
from tastypie.resources import ModelResource, Resource
from tastypie.authorization import Authorization
from tastypie.utils import dict_strip_unicode_keys
from tastypie.validation import Validation
from WebComponents.CalcEngine import calculateHedgefundvalue
import cPickle
import json
from tastypie import http



class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class SimulationModelResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = SimulationModel.objects.all()
        authorization = Authorization()
        resource_name = 'simulationmodel'
        always_return_data = True
    
    
    # Override the post_list method from ModelResources, for associating a simulation run with every SimulationModel object
    # created. As soon as the object is created (before commit to database), we trigger the simulation. This might be    
    # CHANGED LATER for a more sound DB design.
    def post_list(self, request, **kwargs):
        
        # Deserialize the body of the request (as the JSON is stringified at JS end)
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        
        # If the data needs to be altered in any sense, override the below method. Currently it does nothing.
        deserialized = self.alter_deserialized_detail_data(request, deserialized)

        # Convert the unicode dictionary into an ASCII key dictionary and build the bundle.
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        
        # CHANGE LATER- Add validation for incoming JSON data
        #self.is_valid(bundle, request)
        
        # The following method creates the database entry for the SImulationModel object, trigger the simulation,
        # and return the simulation output and graph co-ordinates in the updated bundle object
        updated_bundle = self.obj_create(bundle, request=request, **self.remove_api_resource_names(kwargs))         
        location = self.get_resource_uri(updated_bundle)
        
        # Check if the model is set to always return data. In this particular context, the 'if' branch is never taken, and kept
        # only for standardization.
        if not self.Meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            
            # This returns the HTML response to the AJAX call
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)
    
    # Override the obj_create method to not only save the SimulationModel object into the database, but also trigger the simulation,
    # retrieve the result and save it to database, and create the SimulationResult object and wrap it in the bundle to be returned.
    def obj_create(self, bundle, request=None, **kwargs):
        """
        A Object Relational Model(ORM)-specific implementation of ``obj_create``.
        """
        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)
            
        # Save FKs just in case.
        self.save_related(bundle)

        # Save the SimulationModel object.
        bundle.obj.save()

        # Trigger the simulation and wait for the output
        ce_hf_minus_mf_hfalpha_hfleverage = calculateHedgefundvalue.calcHedgefundvalue(bundle.obj)
        
        # CHANGE LATER- the following variables will be returned from the calcHedgefundvalue function
        xaxis_min = 0.0
        xaxis_max = 0.0
        xaxis_div = 0
        yaxis_min = 0.0
        yaxis_max = 0.0
        yaxis_div = 0
        
        # Compress the result array and store it in database
        #outputval = cPickle.dumps(ce_hf_minus_mf_hfalpha_hfleverage)
        outputval = ce_hf_minus_mf_hfalpha_hfleverage
        p = SimulationResult(simInstancekey = bundle.obj, simResultarray = outputval)
        p.save()

        # Create a dictionary of the result object and wrap it in the Bundle
        #result_data = dict([('result',ce_hf_minus_mf_hfalpha_hfleverage), ('xaxis_min', xaxis_min),('xaxis_max',xaxis_max), ('xaxis_div', xaxis_div), \
        #                    ('yaxis_min', yaxis_min),('yaxis_max',yaxis_max), ('yaxis_div', yaxis_div),])        
        #result_bundle = self.build_bundle(obj = p, data=result_data, request=None)   

        # Now pick up the M2M bits.
        m2m_bundle = self.hydrate_m2m(bundle)
        self.save_m2m(m2m_bundle)

        # Return the updated bundle with the simulation result
        return bundle

#  Resource for the Simulation Result
class SimulationResultResource(ModelResource):
    
    # simulationmodel here will give a reference to the parent SimulationModelResource and all the attributes of SimulationModel
    simulationmodel = fields.ToOneField(SimulationModelResource, attribute='simInstancekey', full=True, null=True)

    class Meta:
        queryset = SimulationResult.objects.all()
        authorization = Authorization()
        resource_name = 'simulationresult'
        list_allowed_methods = ['get']

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(SimulationResultResource, self).build_filters(filters)

        if('latestsim' in filters):
            query = filters['latestsim']
            sqs = SimulationModel.objects.select_related('simulationresult').values('simType').annotate(max_id=Max('simulationresult__id')).values('max_id')
            
            orm_filters["pk__in"] = sqs

        return orm_filters
        
    #def full_dehydrate(self, bundle):
    #    """
    #    Given a bundle with an object instance, extract the information from it
    #    to populate the resource.
    #    """
    #    print("here")
    #    # Dehydrate each field.
    #    for field_name, field_object in self.fields.items():
    #        # A touch leaky but it makes URI resolution work.
    #        if getattr(field_object, 'dehydrated_type', None) == 'related':
    #            field_object.api_name = self._meta.api_name
    #            field_object.resource_name = self._meta.resource_name

    #        bundle.data[field_name] = field_object.dehydrate(bundle)

    #        # Check for an optional method to do further dehydration.
    #        method = getattr(self, "dehydrate_%s" % field_name, None)

    #        if method:
    #            bundle.data[field_name] = method(bundle)

    #    bundle = self.dehydrate(bundle)
    #    return bundle

    def dehydrate(self, bundle):
        upd_bundle = Resource.dehydrate(self, bundle)
        return upd_bundle
