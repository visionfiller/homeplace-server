SELECT p.id, p.address, p.square_footage, a.neighborhood, pt.name,p.owner_id, au.first_name  || ' ' || au.last_name as full_name
FROM homeplaceapi_property as p 
JOIN homeplaceapi_swapper as s ON s.id = p.owner_id
JOIN homeplaceapi_area as a ON a.id = p.area_id
JOIN homeplaceapi_propertytype as pt ON pt.id = p.property_type_id
JOIN auth_user as au ON au.id = s.user_id