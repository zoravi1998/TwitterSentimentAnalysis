from googletrans import Translator
sent ="बॉलीवुड स्टार्स लगातार कोरोना काल में लोगों की मदद के लिए आगे आ रहे हैं. अस्पतालों में ऑक्सीजन सिलेंडर और बेड की कमी के कारण, एक्टर्स अपने स्तर पर मदद कर रहे हैं."
print(sent)
translator = Translator()
#sent=str(sent.encode('unicode-escape').decode())
translations = translator.translate(sent,dest="en")
print(translations.text.encode('utf-8'))