from datetime import datetime
import constants


class ClientArticle:
    all_articles = []

    def __init__(self, card_id, article_title, card_url, surfer_seo, final_link, word_count,
                 writer, completed_date: datetime, client, sheet):
        self.card_id = card_id
        self.article_title = article_title
        self.card_url = card_url
        self.surfer_seo = surfer_seo
        self.final_link = final_link
        self.word_count = word_count
        self.writer = writer
        self.completed_date = completed_date.strftime(constants.DATE_FORMAT)
        self.client = client
        self.sheet = sheet

        if self.surfer_seo is not None:
            self.article_link = self.surfer_seo
        else:
            self.article_link = self.final_link

        ClientArticle.all_articles.append(self)

    def __repr__(self):
        return f"ClientArticle('{self.card_id}', '{self.article_title}', " \
               f"'{self.card_url}', '{self.surfer_seo}', " \
               f"'{self.final_link}', '{self.word_count}', " \
               f"'{self.writer}', '{self.completed_date}', " \
               f"'{self.client}', '{self.sheet}')"

    def return_spreadsheet_value(self):
        return [self.card_id, self.article_title, self.card_url, self.article_link,
                self.word_count, self.writer, self.completed_date, self.client, 'Written']

    @staticmethod
    def instantiate_from_db_list(db_rows):
        for row in db_rows:
            ClientArticle(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

    @staticmethod
    def return_articles_by_sheet(sheet):
        list_of_articles = []

        for article in ClientArticle.all_articles:
            if article.sheet == sheet:
                list_of_articles.append(article.return_spreadsheet_value())

        return list_of_articles

    @staticmethod
    def return_james_articles():
        james_articles = []
        for article in ClientArticle.all_articles:
            if article.client == 'James Thompson':
                james_articles.append(article)

        return james_articles

    @staticmethod
    def update_article_status():
        values = []
        for article in ClientArticle.all_articles:
            values.append([3, article.card_id])

        return values
