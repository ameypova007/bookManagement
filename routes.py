from flask import Flask, request, redirect
from flaskext.mysql import MySQL
import pymysql
from flask import jsonify


app = Flask(__name__)
connection= pymysql.connect("HOST_NAME","DB_USER_NAME","DB_PASSWORD","DB_NAME")
cursor = connection.cursor()

error_data={'KEY_ERROR':400}


def findBook(bookId, language, author, topic, title, mimeType, pageNumber):
    finalResponse = {}

    if(bookId == None and language == None and author == None and title == None and mimeType == None and topic == None):

        # Query to get final result.
        executionQuery = f"""select bb.title, ba.birth_year, ba.death_year, ba.name as author_name, bl.code, bsub.name as
                       subject_name, bsh.name as bookshelf_name, bb.download_count, bf.mime_type, bf.url from books_book bb
                       left join books_book_authors bba on bba.book_id = bb.id
                       left join books_book_languages bbl on bbl.book_id = bb.id
                       left join books_book_bookshelves bbsh on bbsh.book_id = bb.id
                       left join books_format bf on bf.book_id = bb.id
                       left join books_book_subjects bbsub on bbsub.book_id = bb.id
                       left join books_author ba on bba.author_id = ba.id
                       left join books_language bl on bbl.language_id = bl.id
                       left join books_bookshelf bsh on bbsh.bookshelf_id = bsh.id
                       left join books_subject bsub on bbsub.subject_id = bsub.id order by bb.download_count desc LIMIT {(pageNumber - 1) * 25}, 25"""

        # To get total number of matched records.
        countQuery = f"select count(*) from ({executionQuery}) as total"

        # Execute query to get result set.
        cursor.execute(executionQuery)
        resultSet = cursor.fetchall()

        # Excute query to get the count.
        cursor.execute(countQuery)
        count = cursor.fetchall()

        finalResponse = prepareResponseObj(resultSet, count)

    elif(bookId != None and language != None and author != None and title != None and mimeType != None and topic != None):

        if(len(bookId) == 0 and len(language) == 0 and len(author) == 0 and len(title) == 0 and len(mimeType) == 0 and len(topic) == 0):

            # Query to get final result.
            executionQuery = f"""select bb.title, ba.birth_year, ba.death_year, ba.name as author_name, bl.code, bsub.name as
                           subject_name, bsh.name as bookshelf_name, bb.download_count, bf.mime_type, bf.url from books_book bb
                           left join books_book_authors bba on bba.book_id = bb.id
                           left join books_book_languages bbl on bbl.book_id = bb.id
                           left join books_book_bookshelves bbsh on bbsh.book_id = bb.id
                           left join books_format bf on bf.book_id = bb.id
                           left join books_book_subjects bbsub on bbsub.book_id = bb.id
                           left join books_author ba on bba.author_id = ba.id
                           left join books_language bl on bbl.language_id = bl.id
                           left join books_bookshelf bsh on bbsh.bookshelf_id = bsh.id
                           left join books_subject bsub on bbsub.subject_id = bsub.id order by bb.download_count desc LIMIT {(pageNumber - 1) * 25}, 25"""

            # To get total number of matched records.
            countQuery = f"select count(*) from ({executionQuery}) as total"

            # Execute query to get result set.
            cursor.execute(executionQuery)
            resultSet = cursor.fetchall()

            # Excute query to get the count.
            cursor.execute(countQuery)
            count = cursor.fetchall()

            finalResponse = prepareResponseObj(resultSet, count)

    else:
        # Query for Join.
        joinQuery = """select bb.title, ba.birth_year, ba.death_year, ba.name as author_name, bl.code, bsub.name as
                       subject_name, bsh.name as bookshelf_name, bb.download_count, bf.mime_type, bf.url from books_book bb
                       left join books_book_authors bba on bba.book_id = bb.id
                       left join books_book_languages bbl on bbl.book_id = bb.id
                       left join books_book_bookshelves bbsh on bbsh.book_id = bb.id
                       left join books_format bf on bf.book_id = bb.id
                       left join books_book_subjects bbsub on bbsub.book_id = bb.id
                       left join books_author ba on bba.author_id = ba.id
                       left join books_language bl on bbl.language_id = bl.id
                       left join books_bookshelf bsh on bbsh.bookshelf_id = bsh.id
                       left join books_subject bsub on bbsub.subject_id = bsub.id where """

        # Array for WHERE clause handling.
        whereQuery = []

        if(bookId != None):
            if(len(bookId)!=0):
                whereQuery.append("(")
                if(len(bookId) == 1):
                    whereQuery.append(f"bb.gutenberg_id = {bookId[0]}")
                else:
                    bookIdTuple = tuple(bookId)
                    whereQuery.append("bb.gutenberg_id in {}".format(bookIdTuple))
                whereQuery.append(" ) AND")


        if(language != None ):
            if(len(language)!=0):
                whereQuery.append("(")
                if(len(language) == 1):
                    whereQuery.append(f" bbl.language_id in (select id from books_language where code = '{language[0]}')")
                else:
                    for i in range(len(language)):
                        whereQuery.append(f" bbl.language_id in (select id from books_language where code = '{language[i]}')")
                        if i != (len(language)-1):
                            whereQuery.append(" or")
                whereQuery.append(") AND")

        if(author != None):
            if(len(author)!=0):
                whereQuery.append("(")
                if(len(author) == 1):
                    whereQuery.append(f" bba.author_id in (select id from books_author where name like '%{author[0]}%')")
                else:
                    for i in range(len(author)):
                        whereQuery.append(f" bba.author_id in (select id from books_author where name like '%{author[i]}%')")
                        if i != (len(author)-1):
                            whereQuery.append(" or")
                whereQuery.append(") AND")

        if(topic != None):
            if(len(topic)!=0):
                whereQuery.append("(")
                if(len(topic) == 1):
                    whereQuery.append(f""" bbsub.subject_id in (select id from books_subject where name like '%{topic[0]}%') or  
                                          bbsh.bookshelf_id in (select id from books_bookshelf where name like '%{topic[0]}%')""")
                else:
                    for i in range(len(topic)):
                        whereQuery.append(f""" bbsub.subject_id in (select id from books_subject where name like '%{topic[i]}%') or  
                                          bbsh.bookshelf_id in (select id from books_bookshelf where name like '%{topic[i]}%')""")
                        if i != (len(topic)-1):
                            whereQuery.append(" or")
                whereQuery.append(") AND")

        if(mimeType != None):
            if(len(mimeType)!=0):
                whereQuery.append("(")
                if(len(mimeType) == 1):
                    whereQuery.append(f" bf.mime_type = '{mimeType[0]}'")
                else:
                    for i in range(len(mimeType)):
                        whereQuery.append(f" bf.mime_type = '{mimeType[i]}'")
                        if i != (len(mimeType)-1):
                            whereQuery.append(" or")
                whereQuery.append(") AND ")


        if(title != None):
            if(len(title)!=0):
                whereQuery.append("(")
                if(len(title) == 1):
                    whereQuery.append(f" bb.title like '%{title[0]}%'")
                else:
                    for i in range(len(title)):
                        whereQuery.append(f" bb.title like '%{title[i]}%'")
                        if i != (len(title)-1):
                            whereQuery.append(" or")
                whereQuery.append(") AND ")


        # To join all WHERE clause conditions.
        whereComplete = " ".join(whereQuery)

        # To combine join query and all WHERE clause conditions.
        combinedQuery = joinQuery + whereComplete

        # Query to get final result.
        executionQuery = combinedQuery[0:len(combinedQuery) - 4] + f" order by bb.download_count desc LIMIT {(pageNumber - 1) * 25}, 25;"

        # To get total number of matched records.
        countQuery = f"select count(*) from ({combinedQuery[0:len(combinedQuery) - 4]}) as total"

        
        # Execute query to get result set.
        cursor.execute(executionQuery)
        resultSet = cursor.fetchall()

        # Excute query to get the count.
        cursor.execute(countQuery)
        count = cursor.fetchall()

        finalResponse = prepareResponseObj(resultSet, count)

    return finalResponse

def prepareResponseObj(bookData, bookCount):
    dictList = [{'count' : bookCount[0]}, {'bookObject' : []}]
    titleName = []

    # dictList['bookObject']={}
    for i in bookData:
        dataDict={}
        dataDict['title'] = i[0]
        dataDict['authorInformation'] = [{"birthYear" : i[1],"deathYear" : i[2],"name" : i[3]}]
        dataDict['language'] = i[4]
        dataDict['subjectName'] = i[5]
        dataDict['bookShelfName'] = i[6]
        dataDict['downloadCount'] = i[7]
        dataDict['mimeType'] = i[8]
        dataDict['url'] = i[9]
        dictList[1]['bookObject'].append(dataDict)
    
    return dictList


@app.route('/searchBook', methods=['GET'])
def searchBook():
    resultDict={}

    try:
        # get request parameters from JSON i/p
        req = request.get_json()

        bookId = req["bookId"]
        if(bookId != None):
            for i in bookId:
                if(type(i) != int):
                    raise ValueError(f"{i} is not of data type int.")
        language = req["language"]
        mimeType = req["mimeType"]
        topic = req["topic"]
        author = req["author"]
        title = req["title"]
        pageNo = req['pageNumber']
        if(pageNo != None):
            if(type(pageNo)!= int):
                raise ValueError(f"{pageNo} is not of data type int.")
            elif(pageNo <= 0):
                raise ValueError("Page number must be a positive integer value")

        else:
            raise ValueError("Page number must be a single integer value, must not be null")

        bookData = findBook(bookId, language, author, topic, title, mimeType, pageNo)

        return jsonify(bookData)

    except ValueError as v:
        resultDict['code'] = error_data['KEY_ERROR']
        print(v)
        resultDict['message'] = f"{v}"
        return jsonify(resultDict)

    except KeyError as k:
        resultDict['code'] = error_data['KEY_ERROR']
        resultDict['message'] = f'Key is not present : {k}. Value can be null or an empty array'
        return jsonify(resultDict)

    except TypeError as t:
        resultDict['message'] = f'Error : {t}'
        return jsonify(resultDict)

    except Exception as e:
        resultDict['message'] = e
        return jsonify(resultDict)



if __name__ == '__main__':
	app.debug = True
	app.run()
