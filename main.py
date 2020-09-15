import sys
import argparse
from datetime import datetime
import src.operations as op
import src.pdf as pdf





def checkDates(date_str, minDate=datetime.strptime("01/01/1995", '%m/%d/%Y'), maxDate=datetime.strptime("12/31/2020", '%m/%d/%Y')):
    date = datetime.now()
    try:
       date = datetime.strptime(date_str, '%m/%d/%Y')
    except Exception:
         raise argparse.ArgumentTypeError(f"{date_str} is an invalid date, must be MM/DD/YYYY format")
     
    if date >= minDate and date < maxDate:
        return date
    else:
        raise argparse.ArgumentTypeError(f"Date must be between {minDate} and {maxDate}")

def main():
    parser = argparse.ArgumentParser(description='Introduces una ciudad y un rango de fechas')
    parser.add_argument('-c', dest='city', default="", help='la ciudad de la que quieras obtener la información')
    parser.add_argument('-s', dest='start_date', default="01/01/1995", type=checkDates, help='la fecha por la que quieres empezar a obtener información. En formato mm/dd/yy.')
    parser.add_argument('-e', dest='end_date', default= '09/13/2020', type=checkDates, help="la fecha por la que quieres terminar de obtener información.En formato mm/dd/yy.")
    parser.add_argument('-t', dest='max_temperature', default= '', help="la temperatura por la que quieres filtrar la información.")

    args = parser.parse_args()
    print(args)
    city = args.city
    start_date = args.start_date
    end_date = args.end_date
    
    op.importCsv()
    plot_df = op.filterDataFrame(op.temp, city, start_date, end_date)
    if start_date.year >= 2020:
        dataFrameAPI = op.dataframeCallingAPI(city, start_date, end_date)
        avgTempDataFrame = op.avgTemp(dataFrameAPI)
        op.plotDataFrame(avgTempDataFrame, city)
    else:
        op.plotDataFrame(plot_df, city)
    if city != "":
        prcpDataFrame = op.callingApiForYears(start_date, end_date, city)
        op.rainChange(prcpDataFrame)

    if args.max_temperature != "":
        max_temp = int(args.max_temperature)
        op.maxTempByCountry(max_temp)
    pdf.creaPDF()
    
                        
if __name__ == "__main__":
    main()
