import endpoints
from google.appengine.ext import ndb
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from endpoints_proto_datastore.ndb import EndpointsModel
#from ndbunq import Model

#About the structure of the API: 

package = 'Elec_Cards_Api'
# Transitioning an existing model is as easy as replacing ndb.Model with
# EndpointsModel. Since EndpointsModel inherits from ndb.Model, you will have
# the same behavior and more functionality.
#class ProfileModel(EndpointsModel):
  # By default, the ProtoRPC message schema corresponding to this model will
  # have three string fields: attr1, attr2 and created
  # in an arbitrary order (the ordering of properties in a dictionary is not
  # guaranteed).
class ProfileModel(EndpointsModel):
  # By default, the ProtoRPC message schema corresponding to this model will
  # have three string fields: attr1, attr2 and created
  # in an arbitrary order (the ordering of properties in a dictionary is not
  # guaranteed).
  mAddress = ndb.StringProperty()
  mAge = ndb.IntegerProperty()
  mSchool = ndb.StringProperty()
  mName = ndb.StringProperty()
  mAvatar = ndb.StringProperty()
  mGender = ndb.IntegerProperty()
  mPhoneNumber = ndb.StringProperty()
  mWeChat = ndb.StringProperty()
  mUserID = ndb.StringProperty(required=True)
  mUser = ndb.KeyProperty()


class EventModel(EndpointsModel):
  # By default, the ProtoRPC message schema corresponding to this model will
  # have three string fields: attr1, attr2 and created
  # in an arbitrary order (the ordering of properties in a dictionary is not
  # guaranteed).
  mLocation = ndb.StringProperty()
  mName = ndb.StringProperty(required=True)
  mStartTime = ndb.StringProperty()
  mEndTime = ndb.IntegerProperty()
  mEventID = ndb.StringProperty(required=True)
  mCatogory = ndb.IntegerProperty()
  mDescription = ndb.StringProperty()
  mUserID = ndb.StringProperty(repeated = True)
  mUsers = ndb.KeyProperty(kind=UserModel, repeated=True, indexed=True)

class TagsModel(EndpointsModel):

  Major = ndb.StringProperty(repeated = True)
  Expertise = ndb.StringProperty(repeated = True)
  States = ndb.StringProperty(repeated = True)
  Year = ndb.StringProperty(repeated = True)
  Hobbies = ndb.StringProperty(repeated = True)
  Others = ndb.StringProperty(repeated = True)
  mUserID = ndb.StringProperty(required=True)

class AccountModel(EndpointsModel):
  mNickName = ndb.StringProperty()
  mPassword = ndb.StringProperty(required=True)
  mUserID = ndb.StringProperty(required=True)
  mUserType = ndb.StringProperty(required=True)

     
class UserModel(EndpointsModel):
  # By default, the ProtoRPC message schema corresponding to this model will
  # have three string fields: attr1, attr2 and created
  # in an arbitrary order (the ordering of properties in a dictionary is not
  # guaranteed).
  mUserID = ndb.StringProperty(required = True)
  mProfile = ndb.KeyProperty(kind = ProfileModel, indexed=True)
  mTags_self = ndb.KeyProperty(kind = TagsModel, indexed=True)
  mTags_other = ndb.StructuredProperty(TagsModel)
  #mEventID = ndb.StringProperty(repeated=True)
  mEvents = ndb.KeyProperty(kind = EventModel, repeated = True, indexed=True)
  mAccount = ndb.KeyProperty(kind = AccountModel, indexed=True)



# Use of this decorator is the same for APIs created with or without
# endpoints-proto-datastore.
@endpoints.api(name='eleccardsapi', version='v1', description='Elec Cards API')
class ElecCardsApi(remote.Service):

  # Instead of the endpoints.method decorator, we can use ProfileModel.method to
  # define a new endpoints method. Instead of having to convert a
  # ProtoRPC request message into an entity of our model and back again, we
  # start out with a ProfileModel entity and simply have to return one.
  # Since no overrides for the schema are specified in this decorator, the
  # request and response ProtoRPC message definition will have the three string
  # fields attr1, attr2 and created.
  @ProfileModel.method(path='profilemodel', http_method='POST', name='profilemodel.insert')
  def ProfileModelInsert(self, profile_model):
    # Though we don't actively change the model passed in, two things happen:
    # - The entity gets an ID and is persisted
    # - Since created is auto_now_add, the entity gets a new value for created
    profile_model.put()
    return profile_model

  @ProfileModel.query_method(query_fields=('mUserID',),path='profilemodelsbyuserID', name='profilemodel.getbyuserID')
  def ProfileModelbyUserID(self, query):
    return query
  # As ProfileModel.method replaces a ProtoRPC request message to an entity of our
  # model, ProfileModel.query_method replaces it with a query object for our model.
  # By default, this query will take no arguments (the ProtoRPC request message
  # is empty) and will return a response with two fields: items and
  # nextPageToken. "nextPageToken" is simply a string field for paging through
  # result sets. "items" is what is called a "MessageField", meaning its value
  # is a ProtoRPC message itself; it is also a repeated field, meaning we have
  # an array of values rather than a single value. The nested ProtoRPC message
  # in the definition of "items" uses the same schema in ProfileModel.method, so each
  # value in the "items" array will have the fields attr1, attr2 and created.
  # As with ProfileModel.method, overrides can be specified for both the schema of
  # the request that defines the query and the schema of the messages contained
  # in the "items" list. We'll see how to use these in further examples.
  @ProfileModel.query_method(path='profilemodels', name='profilemodels.list')
  def ProfileModelsList(self, query):
    # We have no filters that we need to apply, so we just return the query
    # object as is. As we'll see in further examples, we can augment the query
    # using environment variables and other parts of the request state.
    #when you need to delete all keys. Use the following command.
    #ndb.delete_multi(
      #query.fetch(keys_only=True))
    return query



  @EventModel.method(path='eventmodel', http_method='POST', name='eventmodel.insert')
  def EventModelInsert(self, event_model):
    # Though we don't actively change the model passed in, two things happen:
    # - The entity gets an ID and is persisted
    # - Since created is auto_now_add, the entity gets a new value for created
    event_model.put()
    return event_model

  @EventModel.query_method(query_fields=('mEventID',),path='eventmodelsbyid', name='eventmodel.getbyid')
  def EventModelbyID(self, query):
    return query
  # As EventModel.method replaces a ProtoRPC request message to an entity of our
  # model, EventModel.query_method replaces it with a query object for our model.
  # By default, this query will take no arguments (the ProtoRPC request message
  # is empty) and will return a response with two fields: items and
  # nextPageToken. "nextPageToken" is simply a string field for paging through
  # result sets. "items" is what is called a "MessageField", meaning its value
  # is a ProtoRPC message itself; it is also a repeated field, meaning we have
  # an array of values rather than a single value. The nested ProtoRPC message
  # in the definition of "items" uses the same schema in EventModel.method, so each
  # value in the "items" array will have the fields attr1, attr2 and created.
  # As with EventModel.method, overrides can be specified for both the schema of
  # the request that defines the query and the schema of the messages contained
  # in the "items" list. We'll see how to use these in further examples.
  @EventModel.query_method(query_fields=('mName',),path='eventmodelsbyname', name='eventmodel.getbyname')
  def EventModelbyName(self, query):
    return query

  @EventModel.query_method(path='eventmodels', name='eventmodels.list')
  def EventModelsList(self, query):
    # We have no filters that we need to apply, so we just return the query
    # object as is. As we'll see in further examples, we can augment the query
    # using environment variables and other parts of the request state.
    #when you need to delete all keys. Use the following command.
    #ndb.delete_multi(
     # query.fetch(keys_only=True))
    return query

  @TagsModel.method(path='tagsmodel', http_method='POST', name='tagsmodel.insert')
  def TagsModelInsert(self, Tags_model):
    # Though we don't actively change the model passed in, two things happen:
    # - The entity gets an ID and is persisted
    # - Since created is auto_now_add, the entity gets a new value for created
    Tags_model.put()
    return Tags_model

  @TagsModel.query_method(query_fields=('mUserID',),path='tagsmodelsbyuserID', name='tagsmodel.getbyuserID')
  def TagsModelbyUserID(self, query):
    return query
  # As TagsModel.method replaces a ProtoRPC request message to an entity of our
  # model, TagsModel.query_method replaces it with a query object for our model.
  # By default, this query will take no arguments (the ProtoRPC request message
  # is empty) and will return a response with two fields: items and
  # nextPageToken. "nextPageToken" is simply a string field for paging through
  # result sets. "items" is what is called a "MessageField", meaning its value
  # is a ProtoRPC message itself; it is also a repeated field, meaning we have
  # an array of values rather than a single value. The nested ProtoRPC message
  # in the definition of "items" uses the same schema in TagsModel.method, so each
  # value in the "items" array will have the fields attr1, attr2 and created.
  # As with TagsModel.method, overrides can be specified for both the schema of
  # the request that defines the query and the schema of the messages contained
  # in the "items" list. We'll see how to use these in further examples.
  @TagsModel.query_method(path='tagsmodels', name='tagsmodels.list')
  def TagsModelsList(self, query):
    # We have no filters that we need to apply, so we just return the query
    # object as is. As we'll see in further examples, we can augment the query
    # using environment variables and other parts of the request state.
    #when you need to delete all keys. Use the following command.
    #ndb.delete_multi(
     # query.fetch(keys_only=True))
    return query

  @AccountModel.method(path='accountmodel', http_method='POST', name='accountmodel.insert')
  def AccountModelInsert(self, Account_model):
    # Though we don't actively change the model passed in, two things happen:
    # - The entity gets an ID and is persisted
    # - Since created is auto_now_add, the entity gets a new value for created
    
    Account_model.put()
    return Account_model

  @AccountModel.query_method(query_fields=('mUserID',),
    collection_fields=('mUserType',),
    path='accountmodelsbyuserID', 
    name='accountmodel.getbyuserID')
  def AccountModelbyUserID(self, query):
    return query
  # As AccountModel.method replaces a ProtoRPC request message to an entity of our
  # model, AccountModel.query_method replaces it with a query object for our model.
  # By default, this query will take no arguments (the ProtoRPC request message
  # is empty) and will return a response with two fields: items and
  # nextPageToken. "nextPageToken" is simply a string field for paging through
  # result sets. "items" is what is called a "MessageField", meaning its value
  # is a ProtoRPC message itself; it is also a repeated field, meaning we have
  # an array of values rather than a single value. The nested ProtoRPC message
  # in the definition of "items" uses the same schema in AccountModel.method, so each
  # value in the "items" array will have the fields attr1, attr2 and created.
  # As with AccountModel.method, overrides can be specified for both the schema of
  # the request that defines the query and the schema of the messages contained
  # in the "items" list. We'll see how to use these in further examples.
  @AccountModel.query_method(query_fields=('mUserID','mPassword',),
    collection_fields=('mUserType',), 
    path='accountmodelsverifyUser', 
    name='accountmodel.verifyUser')
  def AccountModelVerifyUser(self, query):
    return query


  @AccountModel.query_method(path='accountmodels', name='accountmodels.list')
  def AccountModelsList(self, query):
    # We have no filters that we need to apply, so we just return the query
    # object as is. As we'll see in further examples, we can augment the query
    # using environment variables and other parts of the request state.
    #when you need to delete all keys. Use the following command.
    #ndb.delete_multi(
      #query.fetch(keys_only=True))
    return query

  @UserModel.method(path='usermodel', http_method='POST', name='usermodel.insert')
  def UserModelInsert(self, User_model):
    # Though we don't actively change the model passed in, two things happen:
    # - The entity gets an ID and is persisted
    # - Since created is auto_now_add, the entity gets a new value for created

    User_model.put()
    return User_model

  @UserModel.query_method(query_fields=('mUserID',),path='usermodelsbyuserID', name='usermodel.getbyuserID')
  def UserModelbyUserID(self, query):
    return query
  # As UserModel.method replaces a ProtoRPC request message to an entity of our
  # model, UserModel.query_method replaces it with a query object for our model.
  # By default, this query will take no arguments (the ProtoRPC request message
  # is empty) and will return a response with two fields: items and
  # nextPageToken. "nextPageToken" is simply a string field for paging through
  # result sets. "items" is what is called a "MessageField", meaning its value
  # is a ProtoRPC message itself; it is also a repeated field, meaning we have
  # an array of values rather than a single value. The nested ProtoRPC message
  # in the definition of "items" uses the same schema in UserModel.method, so each
  # value in the "items" array will have the fields attr1, attr2 and created.
  # As with UserModel.method, overrides can be specified for both the schema of
  # the request that defines the query and the schema of the messages contained
  # in the "items" list. We'll see how to use these in further examples.
  @UserModel.query_method(path='usermodels', name='usermodels.list')
  def UserModelsList(self, query):
    # We have no filters that we need to apply, so we just return the query
    # object as is. As we'll see in further examples, we can augment the query
    # using environment variables and other parts of the request state.
    #when you need to delete all keys. Use the following command.
    #ndb.delete_multi(
     # query.fetch(keys_only=True))
    return query
    

# Use of endpoints.api_server is the same for APIs created with or without
# endpoints-proto-datastore.
APPLICATION = endpoints.api_server([ElecCardsApi], restricted=False)
