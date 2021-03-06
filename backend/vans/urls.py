from django.urls import path
from .views import *



urlpatterns = [
    path('dashboard',Dashboard.as_view(),name='dashboard'),
    path('all',AllSlots.as_view(),name='all_slots'),
    path('best',BestSlots.as_view(),name='best_slots'),
    path('book/',BookSlot.as_view(),name = "book"),
    path('slotlist',ListUser.as_view(),name='slotlist'),
    path('confirm/',UserVaccinated.as_view(),name = "confirm"),
    path('cancel/',Sendgrievancemail.as_view(),name='cancel'),
    path('mark/',LocationMark.as_view(),name='mark'),
    path('vanall',VanALLView.as_view(),name='vanall'),
    path('van/<int:id>',SpecificVan.as_view(),name='specific_van'),
    path('cancelself/',CancelSlotView.as_view(),name='cancel_self'),
]