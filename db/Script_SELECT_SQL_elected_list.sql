SELECT sl.style_name, COUNT(ss.singer_id) FROM style_singer ss 
	JOIN style_list sl ON ss.style_id = sl.id 
	GROUP BY sl.style_name  
	ORDER BY sl.style_name;
	
SELECT COUNT(t.id) FROM track_list t 
	JOIN album_list a ON t.album_id = a.id
	WHERE a.release_year BETWEEN 2019 AND 2020; 
	
SELECT album_id, round(AVG(track_time), 2) FROM track_list 
	GROUP BY album_id
	ORDER BY album_id;
	
SELECT sa.singer_id,  sl.singer_name FROM singer_album sa 
	JOIN album_list al ON sa.album_id = al.id 
	JOIN singer_list sl ON sa.singer_id = sl.id 
	WHERE al.release_year != 2020;
	
SELECT collection_name FROM collection c 
	JOIN collection_track ct ON c.id = ct.collection_id 
	JOIN track_list tl ON ct.track_id = tl.id 
	JOIN album_list al ON tl.album_id = al.id 
	JOIN singer_album sa ON al.id = sa.album_id 
	JOIN singer_list sl ON sa.singer_id = sl.id 
	WHERE sl.singer_name = 'Trololo'
	ORDER BY collection_name; 
	
SELECT album_name FROM album_list al 
	JOIN singer_album sa ON al.id = sa.album_id 
	JOIN singer_list sl ON sa.singer_id = sl.id
	JOIN style_singer ss ON sl.id = ss.singer_id 
	JOIN style_list sl2 ON ss.style_id = sl2.id
	GROUP BY album_name 
	HAVING COUNT(style_id) > 1
	ORDER BY album_name;
	
SELECT track_name FROM track_list tl 
	LEFT JOIN collection_track ct ON tl.id = ct.track_id 
	WHERE ct.track_id IS NULL 
	ORDER BY track_name;
	
SELECT sl.singer_name, track_name, track_time FROM track_list tl
	JOIN album_list al ON tl.album_id = al.id 
	JOIN singer_album sa ON al.id = sa.album_id 
	JOIN singer_list sl ON sa.singer_id = sl.id 
	WHERE track_time = (SELECT MIN(track_time) FROM track_list);	
	
 SELECT al.album_name, COUNT(tl.id) FROM album_list al
    JOIN track_list tl ON al.id = tl.album_id
    GROUP BY al.album_name 
    HAVING COUNT(tl.id) IN (
    SELECT COUNT(tl.id) FROM album_list al
    JOIN track_list tl ON al.id = tl.album_id
    GROUP BY al.album_name 
    ORDER BY COUNT(tl.id)
    LIMIT 1);
	
