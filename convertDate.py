# fmt = "%Y-%m-%d %H:%M:%S %Z%z"
fmt = "%Y-%m-%d %H:%M:%S"
now_utc = datetime.now(timezone('UTC'))
now_central = now_utc.astimezone(timezone('US/Central'))
formattedDate = now_central.strftime(fmt)
# print(formattedDate)