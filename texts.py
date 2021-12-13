class Texts:

    m = {
        "No Data": {
            "en": "No current data; sensor is disconnected",
            "he": "אין מידע זמין; חיישן מנותק"
        },
        "Good": {
            "en": "<b>0-10: Good.</b>%0a%0aThe air quality is good. Enjoy your usual outdoor activities.",
            "he": "<b>0-10: טוב.</b>%0a%0aאיכות האוויר טובה. תהנו בחוץ."
        },
        "Fair": {
            "en": "<b>10-20: Fair.</b>%0a%0aEnjoy your usual outdoor activities.",
            "he": "<b>10-20: סביר.</b>%0a%0aאיכות האוויר סבירה. תהנו בחוץ."
        },
        "Moderate": {
            "en": "<b>20-25: Moderate.</b>%0a%0aEnjoy your usual outdoor activities.%0aSensitive groups should consider reducing intense outdoor activities, if you experience symptoms.",
            "he": "<b>20-25: בינוני.</b>%0a%0aתהנו בחוץ.%0aקבוצות רגישות צריכות לשקול להפחית בפעילויות חוץ אינטנסיביות, במידה וחווים תסמינים."
        },
        "Poor": {
            "en": "<b>25-50: Poor.</b>%0a%0aConsider reducing intense activities outdoors, if you experience symptoms such as sore eyes, a cough or sore throat.%0aSensitive groups should consider reducing physical activities, particularly outdoors, especially if you experience symptoms.",
            "he": "<b>25-50: ירוד.</b>%0a%0aשקלו להפחית בפעילויות חוץ אינטנסיביות, אם הינכם חווים תסמינים כגון כאב בעיניים, שיעול או צריבה בגרון.%0aקבוצות רגישות צריכות לשקול להפחית בפעילות גופנית, בעיקר בחוץ, ובפרט אם הינכם חווים תסמינים."
        },
        "Very Poor": {
            "en": "<b>50-75: Very Poor.</b>%0a%0aConsider reducing intense activities outdoors, if you experience symptoms such as sore eyes, a cough or sore throat.%0aSensitive groups should reduce physical activities, particularly outdoors, especially if you experience symptoms.",
            "he": "<b>50-75: ירוד מאד.</b>%0a%0aשקלו להפחית בפעילויות חוץ אינטנסיביות, אם הינכם חווים תסמינים כגון כאב בעיניים, שיעול או צריבה בגרון.%0aקבוצות רגישות צריכות להפחית בפעילות גופנית, בעיקר בחוץ, ובפרט אם הינכם חווים תסמינים."
        },
        "Extremely Poor": {
            "en": "<b>over 75! Extremely Poor.</b>%0a%0aReduce physical activities outdoors.%0aSensitive groups should avoid physical activities outdoors.",
            "he": "<b>מעל 75! ירוד ביותר.</b>%0a%0aצמצמו בפעילויות חוץ אינטנסיביות.%0aקבוצות רגישות צריכות להימנע מפעילות גופנית בחוץ."
        }
    }

    def __init__(self, locale: str):
        self.locale = locale

    def t(self, key):
        _text = self.m.get(str(key))
        return (_text.get(self.locale) or _text.get("en")) if _text else key
