from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter(trailing_slash = False)
router.register('temple',TempleView)
router.register('temple_main_category', TempleMainCategoryViewSet, basename='temple_main_category')  

router.register("templeCategeory",templeCategeoryview)
router.register("templepriority",TemplePriorityView)
router.register('goshalacategories', GoshalaCategoryViewSet)
router.register("eventcategory",EventCategoryView)
router.register("goshala",GoshalaView)
router.register("event",EventView)
router.register("country",CountryViews,basename='country')
router.register('state',StateViews)
router.register("district",DistrictVIew)
router.register("block",BlockView)
router.register("village",VillageView)
router.register("comment",CommentView)
# router.register("famoustemples",FamousTempleListCreateView)
router.register("connect",ConnectView)
# router.register("member",MemberView)
# router.register("register",Registerview)
# router.register("allvillages",GetVillages)
router.register("chat",ChatViews)
router.register("add_more_temple_details",AddTempleDetailsView)
router.register("add_more_event_details",AddEventDetailsView)
router.register("add_more_goshala_details",AddGoshalaDetailsView)
router.register("add_more_village_details",AddVillageDetailsView)
router.register("media",MediaView)
router.register("tourism",TempleNearbyTourismPlacesView)
router.register("temple-nearby-hotels",TempleNearbyHotelView)
router.register('temple-transports', TempleTransportViewSet)
router.register('tour-operators', TourOperatorViewSet)
router.register('tour_guides', TourGuideViewSet)
# router.register('temple_festivals', TempleFestivalViewSet)
router.register('nearby_hospitals', NearbyHospitalViewSet)
router.register('social_activities', SocialActivityViewSet)
router.register('prayers_and_benefits', PrayersAndBenefitsViewSet)
router.register('temple_facilities', TempleFacilitiesViewSet)
router.register('temple_pooja_timings', TemplePoojaTimingViewSet)
router.register('favorite-temples', FavoriteTempleViewSet, basename='favorite-temple')
router.register('pujari_category', PujariCategeoryview)
router.register('pujari-subcategories', PujariSubCategoryViewSet)
router.register('restaurants', TempleNearbyRestaurantView, basename='temple-nearby-restaurant')
router.register('visit_temples', VisitTempleViewSet)
router.register('ambulance_facility', AmbulanceFacilityView)
router.register('blood_bank', BloodBankView)
router.register('fire_station', FireStationView)
router.register('police_station', PoliceStationView)
router.register('pooja_stores', PoojaStoreView)
router.register('veterinary_hospital', NearbyVeterinaryHospitalViewSet)
router.register("accommodation",AccommodationView)
router.register('village-famous-personalities', VillageFamousPersonalityViewSet)
router.register('village-artists', VillageArtistViewSet)
router.register('village-development-facilities', VillageDevelopmentFacilityViewSet)
router.register('village-cultural-profile', VillageCulturalProfileViewSet)
router.register('village_geographic', VillageGeographicViewSet)
router.register('village_school', VillageSchoolViewSet)
router.register('village-bank',VillageBankViewSet)
router.register('village-college',VillageCollegeViewSet)
router.register('village-market',VillageMarketViewSet)
router.register('village-postoffice',VillagePostOfficeViewSet)
router.register('village-sportsground',VillageSportsgroundViewSet)
router.register('welfare_homes_category',WelfareHomesCategoryViewSet)
router.register('welfare_home',WelfareHomesViews)
router.register('add_more_restaurants', AddRestaurantDetailsView, basename='restaurants')
router.register('add_more_tour-operators', AddTourOperatorViewSet, basename='tour-operators')
router.register('add_more_blood_bank', AddMoreBloodBankViewSet, basename='add-more-blood-bank')
router.register('add_more_veterinary_hospital', AddMoreVeterinaryHospitalViewSet, basename='add-more-veterinary-hospital')
router.register('add_more_pooja_store', AddMorePoojaStoreViewSet, basename='add-more-pooja-store')
router.register('add_more_hotel', AddMoreHotelViewSet, basename='add-more-temple-hotel')
router.register('add_more_hospital', AddMoreHospitalViewSet, basename='add-more-nearby-hospital')
router.register('add_more_tourismplaces',AddTourismPlaceViewSet)
router.register('add_more_welfarehomes',AddWelfareHomeViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path("templemain",TempleMain.as_view()),
    path("goshalamain",GoshalaMain.as_view()),
    path("eventsmain",EventsMain.as_view()),
    path("register",Registerview.as_view()),
    path("verify",LoginView.as_view()),
    # path("verify",VerifyOtpView.as_view()),
    path("home",HomeView.as_view()),
    path('templeget/<str:field_name>/<str:input_value>', GetItemByfield_InputView.as_view()),
    path('temple_inactive_get/<str:field_name>/<str:input_value>', GetInactiveTempleByFieldView.as_view()),
    path('events_inactive_get/<str:field_name>/<str:input_value>/', GetInactiveEventByFieldView.as_view()),
    path('goshala_inactive_get/<str:field_name>/<str:input_value>/', GetInactiveGoshalaByFieldView.as_view()),
    path('village_inactive_get/<str:field_name>/<str:input_value>/', GetInactiveVillageByFieldView.as_view()),


    path("templepost",Templepost.as_view()),
    path("goshalapost",GhoshalaPost.as_view()),
    path("eventpost",EventPost.as_view()),
    # path('temple/by_state/<str:stateid>/', GetItemByfield_location.as_view(), name='temple-by-state'),
    path("indiatemples",GetIndianTemples.as_view()),
    path("globaltemples",GetGlobalTemples.as_view()),
    path('temples/state_id/<str:state_id>/', GetItemByfield_location.as_view()),
    path('temples/district_id/<str:district_id>/', GetbyDistrictLocationTemples.as_view()),
    path('temples/block_id/<str:block_id>/', GetbyBlockLocationTemples.as_view()),
    path('temples/country_id/<str:country_id>/',GetbyCountryLocationTemples.as_view()),
    path('goshalas/state_id/<str:state_id>/', GetbyStateLocationGoshalas.as_view()),
    path('goshalas/district_id/<str:district_id>/', GetbyDistrictLocationGoshalas.as_view()),
    path('goshalas/block_id/<str:block_id>/', GetbyBlockLocationGoshalas.as_view()),
    path('Events/state_id/<str:state_id>/', GetbyStateLocationEvents.as_view()),
    path('Events/district_id/<str:district_id>/', GetbyDistrictLocationEvents.as_view()),
    path('Events/block_id/<str:block_id>/', GetbyBlockLocationEvents.as_view()),
    path('eventsstatus', EventstatusView.as_view(), name='event-list'),
    path('indiaevents',GetIndianEvents.as_view()),
    path('globalevents',GetGlobalEvents.as_view()),
    path('globalgoshala',GetGlobalGoshalas.as_view()),
    path('indiagoshalas',GetIndianGoshalas.as_view()),
    #  path('api/temples/<str:input_value1>/<str:field_name1>/<str:input_value2>/<str:field_name2>/', filters_by_iteams.as_view(), name='get_item_by_two_fields'),
    path('api/temples/', filters_by_iteams.as_view(), name='get_item_by_fields'),

    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    #  path('locationByTemples/<str:input_value>/',GetTemplesByLocation.as_view()),  
    path('locationByTemples/', GetTemplesByLocation.as_view(), name='get_temples_by_location'),
    path('locationByGoshalas/', GetGoshalasByLocation.as_view(), name='get_goshala_by_location'),
    path('locationByEvents/', GetEventsByLocation.as_view(), name='get_events_by_location'),
    path('profileimages/<str:id>',ProfileUpdate.as_view()),
    path('profile_get/',GetProfile.as_view()),
    path('profile_get_by_id/<str:id>/',GetProfileById.as_view()),
    path('profile/<str:id>',updateprofile.as_view()),
    path('templedetail/<str:pk>/', TempleDetailView.as_view(), name='temple-detail'),
    path('deleteimage/<str:id>',DeleteImage.as_view()),
    path("updateroots/<str:id>", updateRoots.as_view()),
    path('search_village/', search_village, name='search_village'),
    path('profile_delete/<uuid:id>/', DeleteProfileView.as_view(), name='delete-profile'),
    path('events_inactive', EventInactiveViewSet.as_view(), name='inactive-events'),
    path('goshala_inactive', InactiveGoshalaAPIView.as_view(), name='inactive-goshala'),
    path('village_inactive', InactiveVillageAPIView.as_view(), name='inactive-village'),
    path('temple_inactive', InactiveTempleAPIView.as_view(), name='inactive-temple'),
    path('tourism_inactive', InactiveTourismPlaceAPIView.as_view(), name='inactive-tourism'),
    path('welfarehomes_inactive', InactiveWelfareHomesAPIView.as_view(), name='welfarehomes'),
    path('inactive_bloodbanks', InactiveBloodBankAPIView.as_view(), name='inactive-bloodbanks'),
    path('inactive_touroperators', InactiveTourOperatorAPIView.as_view(), name='inactive-touroperators'),

    # path('temple-nearby-hotels', TempleNearbyHotelListCreateView.as_view(), name='temple_nearby_hotels'),
    # path('temple-nearby-tourism-places', TempleNearbyTourismPlacesView.as_view(), name='temple-nearby-tourism-places'),

    path('InactivelocationByTemples', GetInactiveTemplesByLocation.as_view(), name='get_temples_by_location'),
    path('InactivelocationByEvents', GetInactiveEventsByLocation.as_view(), name='get_events_by_location'),
    path('InactivelocationByGoshalas', GetInactiveGoshalasByLocation.as_view(), name='get_goshala_by_location'),
    path('citytemples_bylocation', GetCityTemplesByLocation.as_view(), name='city_temples_by_location'),
    path('towntemples_bylocation', GetTownTemplesByLocation.as_view(), name='town_temples_by_location'),
    path('statetemples_bylocation', GetStateTemplesByLocation.as_view(), name='state_temples_by_location'),

    path('tourism_bylocation', GetTourismByLocation.as_view(), name='tourism-by-location'),

    path('inactive_tourism_bylocation', GetInactiveWelfareHomesByLocation.as_view(), name='inactive_tourism-by-location'),


    path('delete-member/<str:id>/', DeleteMemberView.as_view(), name='delete-member'),
    path('delete-pujari/<str:id>/', DeletePujariView.as_view(), name='delete-pujari'),
    path('villages_by_location', GetVillagesByLocation.as_view(), name='get-villages-by-location'),
    path("templemerge/<str:temple_id>/", AddmoretempledetailtemplemergeAPIView.as_view()),
    path("mergevillage/<str:village_id>/", AddmorevillagedetailvillagemergeAPIView.as_view()),
    path('inactive_welfare_homes_by_location', GetInactiveWelfareHomesByLocation.as_view(), name='inactive_welfare-homes-by-location'),

    path('welfare-homes_by-location', GetWelfareHomesByLocation.as_view(), name='welfare-homes-by-location'),
    path('share/<str:content_type>/<str:content_id>/', ShareContentView.as_view(), name='share-content'),
    path("share/temple/<str:id>/", ShareTemplePageView.as_view(), name="share-temple-page"),
    path('pooja_stores_by_location',GetPoojaStoresByLocation.as_view(),name='pooja-stores-by-location'),
    path('hospitals_by_location',GetHospitalsByLocation.as_view(),name='nearby-hospitals-by-location'),
    path('blood_banks_by_location',GetBloodBanksByLocation.as_view(),name='blood-banks-by-location'),
    path('veterinary_hospitals_by_location',GetVeterinaryHospitalsByLocation.as_view(),name='veterinary-hospitals-by-location'),
    path('hotels_by_location',GetHotelsByLocation.as_view(),name='hotels-by-location'),
    path('restaurants_by_location',GetRestaurantsByLocation.as_view(),name='restaurants-by-location'),
    path('sso_login', SSOLoginVerify.as_view()),
    path('tour-operators_by_location', TourOperatorsByLocation.as_view()),
    path('tour_guides_by_location', TourGuidesByLocation.as_view()),
    path("eventmerge/<str:event_id>", AddMoreEventDetailEventMergeAPIView.as_view()),
    path("goshalamerge/<str:goshala_id>",AddMoreGoshalaDetailGoshalaMergeAPIView.as_view()),
    path("global_search", GlobalSearchView.as_view(), name="global-search"),
    path("bloodbank_merge/<uuid:blood_bank_id>",BloodBankMergeAPIView.as_view()),
    path("nearby_hospital_merge/<uuid:hospital_id>",HospitalMergeAPIView.as_view()),
    path("temple_hotel_merge/<uuid:hotel_id>",HotelMergeAPIView.as_view()),
    path("pooja_store_merge/<uuid:pooja_store_id>",PoojaStoreMergeAPIView.as_view()),
    path("restaurant_merge/<uuid:restaurant_id>",RestaurantMergeAPIView.as_view()),
    path("tour_operator_merge/<uuid:operator_id>",TourOperatorMergeAPIView.as_view()),
    path("veterinary_hospital_merge/<uuid:operator_id>",VeterinaryHospitalMergeAPIView.as_view()),
    path('admin_profile_get_by_id/<str:id>/',AdminProfileById.as_view()),
    path('Inactive_blood_banks_by_location',GetInactiveBloodBanksByLocation.as_view(),name='blood-banks-by-location'),
    path('Inactive_tour_operator_by_location',InactiveTourOperatorsByLocation.as_view(),name='tour-operator-by-location'),
    path('Inactive_hospitals_by_location',GetInactiveHospitalsByLocation.as_view(),name='hospitals-by-location'),
    path('Inactive_restaurants_by_location',GetInactiveRestaurantsByLocation.as_view(),name='restaurants-by-location'),
    path('Inactive_hotel_by_location',GetInactiveHotelsByLocation.as_view(),name='hotel-by-location'),
    path('Inactive_poojastores_by_location',GetInactivePoojaStoresByLocation.as_view(),name='poojastores-by-location'),
    path('Inactive_veterinary_hospitals_by_location',GetInactiveVeterinaryHospitalsByLocation.as_view(),name='veterinary_hospitals-by-location'),
    path('inactive_tour_guide', InactiveTourGuideAPIView.as_view()),
    path('inactive_geographic', InactiveGeographicAPIView.as_view()),
    path('inactive_hospitals', InactiveNearbyHospitalAPIView.as_view()),
    path('inactive_famous_personality', InactiveFamousPersonalityAPIView.as_view()),
    path('inactive_development_facility', InactiveVillageDevelopmentFacilityAPIView.as_view()),
    path('inactive_cultural_profile', InactiveVillageCulturalProfileAPIView.as_view()),
    path('inactive_village_artist', InactiveVillageArtistAPIView.as_view()),
    path('inactive_transport', InactiveTransportAPIView.as_view()),
    path('inactive_sports_ground', InactiveVillageSportsgroundAPIView.as_view()),
    path('inactive_school', InactiveVillageSchoolAPIView.as_view()),
    path('inactive_postoffice', InactiveVillagePostOfficeAPIView.as_view()),
    path('inactive_policestation', InactivePoliceStationAPIView.as_view()),
    path('inactive_market', InactiveVillageMarketAPIView.as_view()),
    path('inactive_firestation', InactiveFireStationAPIView.as_view()),
    path('inactive_college', InactiveVillageCollegeAPIView.as_view()),
    path('inactive_bank', InactiveVillageBankAPIView.as_view()),
    path('inactive_ambulance', InactiveAmbulanceFacilityAPIView.as_view()),
    path('inactive_accommodation', InactiveAccommodationAPIView.as_view()),

    path('inactive_restaurants', InactiveRestaurantAPIView.as_view(), name='inactive-restaurants'),
    path('inactive_hotel', InactiveHotelAPIView.as_view(), name='inactive-hotel'),
    path('inactive_poojastores', InactivePoojaStoreAPIView.as_view(), name='inactive-poojastores'),
    path('inactive_veterinary_hospitals', InactiveVeterinaryHospitalAPIView.as_view(), name='inactive-veterinary_hospitals'),
    path("tourismplaces_merge/<uuid:tourism_id>",TourismPlaceMergeAPIView.as_view()),
    path("welfarehomes_merge/<uuid:welfare_id>",WelfareHomeMergeAPIView.as_view()),
    path("users/", UsersStatusView.as_view()),
    path('status_active/<str:id>',UniversalActivateAPIView.as_view()),
    path("admin/login/", AdminLoginView.as_view()),







    

    
  

]
