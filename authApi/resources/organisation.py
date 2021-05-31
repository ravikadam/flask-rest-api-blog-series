from flask import Response, request
from database.models import Organisation, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, OrganisationAlreadyExistsError, InternalServerError, \
UpdatingOrganisationError, DeletingOrganisationError, OrganisationNotExistsError


class OrganisationApi(Resource):
    def get(self):
        query = Organisation.objects()
        organisations = Organisation.objects().to_json()
        return Response(organisations, mimetype="application/json", status=200)

    #@jwt_required
    def post(self):
        try:
            #user_id = get_jwt_identity()
            body = request.get_json()
            organisation =  Organisation(**body)
            organisation.save()
            id = organisation.id
            return {'id': str(id)}, 200

        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise OrganisationAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class OrganisationsChangeApi(Resource):
   # @jwt_required
    def put(self,id):
        try:
            organisation = Organisation.objects.get(id=id)
            body = request.get_json()
            Organisation.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingOrganisationError
        except Exception:
            raise InternalServerError       
    
    #@jwt_required
    def delete(self,id):
        try:
            organisation = Organisation.objects.get(id=id)
            organisation.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingOrganisationError
        except Exception:
            raise InternalServerError

    def get(self, id):
        try:
            organisations = Organisation.objects.get(id=id).to_json()
            return Response(organisations, mimetype="application/json", status=200)
        except DoesNotExist:
            raise OrganisationNotExistsError
        except Exception:
            raise InternalServerError
