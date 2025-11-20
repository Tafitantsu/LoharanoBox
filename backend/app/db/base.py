# This file is used to import all the models into the Base.metadata
# for Alembic autogeneration.

from app.db.base_class import Base  # Import the Base from a new file
from app.models.user import User, Role, Permission  # Import your models
from app.models.metier import Metier, Secteur, Domaine, SousDomaine
from app.models.reference import CompetenceRef, ActiviteRef, ConditionRef, EquipementRef, AppellationRef
from app.models.suggestion import Suggestion, Source
