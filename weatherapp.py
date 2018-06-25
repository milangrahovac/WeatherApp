from tkinter import *
import requests
import time
from urllib import parse


class YahooWeatherForecast:
    def __init__(self, city, country):
        self.city = city
        self.country = country

    def get_weather(self):

        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='{}, {}') and u='c'".format(self.city, self.country)
        url = baseurl + parse.urlencode({'q': yql_query}) + "&format=json"

        print()
        print(time.strftime('time: %a %d. %b %Y'))
        print("sending HTTP request for {} {}".format(self.city, self.country))
        print()
        data = {}

        try:
            data = requests.get(url).json()
        except TypeError as err:
            print("error: {}".format(err))

        try:
            city_data = data["query"]["results"]["channel"]["description"]
            forecast_data = data["query"]["results"]["channel"]["item"]["forecast"][0]

            forecast = "{}".format(city_data)
            forecast = "{} \n {}".format(forecast, forecast_data["date"])
            high_temp = "max temp {} {}".format(forecast_data["high"], u'\u2103')
            forecast = "{} \n {}".format(forecast, high_temp)

            min_temp = "min temp {} {}".format(forecast_data["low"], u'\u2103')
            forecast = "{} \n {}".format(forecast, min_temp)

            forecast = "{} \n {}".format(forecast, forecast_data["text"])
            print()
            print(forecast)
            print()
            return forecast
        except (TypeError, KeyError) as err:
            print("error: {}".format(err))
        return None


def check_entry_fields(city, country, msg):
    ret = False
    s = ""
    if len(city) == 0 or len(country) == 0:
        s = "Please type city and country!"
        print("{}, {} unesite grad i drzavu".format(city, country))
    else:
        if (city.isnumeric() or city.replace(" ", "").isalpha()) and country.isalpha():
            ret = True
        else:
            s = "Please type correctly city (or city code) and country."

    msg["text"] = s
    msg.pack()
    return ret


def weather(city, country, msg):
    if check_entry_fields(city, country, msg):
        w = YahooWeatherForecast(city, country)
        weather_data = w.get_weather()

        if weather is not None:
            msg["text"] = weather_data
        else:
            err = "Yahoo can not find forecast for <{} {}>. \n".format(city, country)
            err += "Please check spelling."
            msg["text"] = err

    msg.pack()
    msg.place(x=60, y=220)


def main():
    root = Tk()
    root.title("Weather")
    # root.pack(fill=BOTH, expand=1)
    canvas = Canvas(root, width=600, height=400, bd=0, highlightthickness=0)

    message = Label(canvas, font=('Helvetica', 20, 'bold'))
    message["text"] = "Weather App"
    message.pack()
    message.place(x=240, y=10)

    canvas.create_line(100, 40, 500, 40)

    message_city = Label(canvas, font=('Helvetica', 20, 'normal'))
    message_city["text"] = "City:"
    message_city.pack()
    message_city.place(x=100, y=100)

    message_country = Label(canvas, font=('Helvetica', 20, 'normal'))
    message_country["text"] = "Country:"
    message_country.pack()
    message_country.place(x=100, y=140)

    entry_field_city = Entry(canvas)
    entry_field_city.pack()
    entry_field_city.place(x=150, y=100)

    entry_field_country = Entry(canvas)
    entry_field_country.pack()
    entry_field_country.place(x=180, y=140)

    entry_btn = Button(canvas, text="OK", width=10, command=lambda: weather(entry_field_city.get(), entry_field_country.get(), return_message))
    entry_btn.pack()
    entry_btn.place(x=200, y=180)

    return_message = Label(font=('Helvetica', 20, 'normal'))
    return_message.place(x=60, y=200)

    canvas.pack()
    # root.update()
    root.mainloop()


if __name__ == '__main__':
    main()
