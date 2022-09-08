from functions.imageboard import getImages

def getImages(cid, search, booru, rating, offset, username):
    #####################################################################################################################
    # save search queries (only for testing)
    today = datetime.now()
    text_file = open("./storage/search.txt", "a+")
    text_file.write(today.strftime('%Y%m%d;%H%M%S') + ":" + str(username) + ":" + str(cid) + ":" + search + "\n")
    text_file.close()
    # User Agent für URL Request
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    # diverse listen
    urls = list()
    thumbs = list()
    files = list()
    tags = list()

    resultSize = 6
    logger.info("Searchstring: %s", search)
    # no rating filter if 0
    if rating == 0:
        rating = ""
    # if booru 0 = yande.re
    if booru == 0:
        searchString = "https://yande.re/post.xml?limit=100&tags=order:score+" + search + "+" + rating
        page = requests.get(searchString, headers=headers)
        error = 0
        try:
            root = ET.fromstring(page.content)
        except ET.ParseError:
            error = 1
        if error == 0:
            x = int(root.attrib['count'])
            if x > 0:
                y = 1
                breaker = 1
                for child in root:
                    if int(y) > int(offset):
                        urls.append(child.attrib['jpeg_url'])
                        thumbs.append(child.attrib['preview_url'])
                        tags.append(child.attrib['tags'])
                        if breaker == resultSize:
                            break
                        else:
                            breaker = breaker + 1
                    else:
                        y = y + 1
                return urls, thumbs, tags;
            else:
                return 0, 0, 0;
        else:
            return 1, 0, 0;
    if booru == 1:
        searchString = "http://www.gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100&tags=-webm+sort:score+" + search + "+" + rating
        page = requests.get(searchString, headers=headers)
        error = 0
        try:
            root = ET.fromstring(page.content)
        except ET.ParseError:
            error = 1
        if error == 0:
            x = int(root.attrib['count'])
            if x > 0:
                y = 1
                breaker = 1
                for child in root:
                    if int(y) > int(offset):
                        urls.append(child.attrib['file_url'])
                        thumbs.append(child.attrib['preview_url'])
                        tags.append(child.attrib['tags'])
                        if breaker == resultSize:
                            break
                        else:
                            breaker = breaker + 1
                    else:
                        y = y + 1
                return urls, thumbs, tags;
            else:
                return 0, 0, 0;
        else:
            return 1, 0, 0;
    elif booru == 2:
        searchString = "https://delishbooru.com/post/index.xml?tags=" + search + "+" + rating
        page = requests.get(searchString, headers=headers)
        error = 0
        try:
            root = ET.fromstring(page.content)
        except ET.ParseError:
            error = 1
        if error == 0:
            x = int(root.attrib['count'])
            if x > 0:
                y = 1
                breaker = 1
                for child in root:
                    if int(y) > int(offset):
                        urls.append(child.attrib['jpeg_url'])
                        thumbs.append(child.attrib['preview_url'])
                        tags.append(child.attrib['tags'])
                        if breaker == resultSize:
                            break
                        else:
                            breaker = breaker + 1
                    else:
                        y = y + 1
                return urls, thumbs, tags;
            else:
                return 0, 0, 0;
        else:
            return 1, 0, 0;

    # if booru 3 = e621
    elif booru == 3:
        searchString = "https://e621.net/post/index.xml?limit=100&tags=order:score+-foxen+-animated+" + search + "+" + rating
        page = requests.get(searchString, headers=headers)
        root = ET.fromstring(page.content)
        x = int(root.attrib['count'])
        if x > 0:
            breaker = 1
            y = 1
            for z in range(0, x):
                if int(y) > int(offset):
                    urls.append(root[z].find('file_url').text)
                    thumbs.append(root[z].find('preview_url').text)
                    tags.append(root[z].find('tags').text)
                    if breaker == resultSize:
                        break
                    else:
                        breaker = breaker + 1
                else:
                    y = y + 1
            return urls, thumbs, tags;
        else:
            return 0, 0, 0;