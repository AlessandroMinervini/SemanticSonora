from .classes import TypeSearch, Response, Error, Status
from .init_logger import logger
    

def sp_search(client, query, type, p_limit = 3):
    try:
        results = []

        response = client.search(q=query, type=type)
        
        objs = response[TypeSearch().filter_type(type)]
        items = objs['items']
        

        if type == "playlist":
            logger.info("Searching playlist into spotify...")
            results = [{"external_urls": i["external_urls"]["spotify"],
                                "images": i["images"],
                                "name": i["name"],
                                "uri": i["uri"]} for i in items]
        
        elif type == "track":
            logger.info("Searching track image into spotify...")
            item = items[0]
            results = item["album"]["images"]

        logger.info("Spotify search end.")
        return results[0:p_limit] if type == "playlist" else results

    except Error as e:
        logger.error(f"{e}")

        return Response(
            status=Status.NOT_FOUND,
            status_message=e.status_message,
        )
