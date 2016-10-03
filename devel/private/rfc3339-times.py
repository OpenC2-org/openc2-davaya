import re

times = [
    "2013-03-25T12:42:31+00:32",
    "2013-03-25T08:10:31-04:00",
    "9998-73-95T08:10:93-47:89",            # OK - regex does no range checking
    "2013-03-25T21:39:35Z",
    "2013-03-25T22:04:01.04399Z",
                                        #----- Bad examples -----
    "20130325T21:39:35Z",                   # no dashes
    "95-03-25T08:10:31-04:00",              # 2 digit year
    "2013-03-25T22:04:01.Z",                # decimal point with no fraction
    "2013-03-25T22:04:03.1415926535897932384626433832795Z",   # valid but silly - allow only 6 fractional digits
    ]

durations = [
    "PT1800S",
    "PT5H97M34S",
    "PT2H35M",
    "PT5M90S",
                        # ----- Bad examples -----
    "PT32M5H15S",           # out of order
    "PT5H15S",              # missing minutes
]

time_regex = "^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d{1,6})?(Z|[-+]\d\d:\d\d)$"
dur_regex = "^PT(\d+H(\d+M(\d+S)?)?|\d+M(\d+S)?|\d+S)$"

if __name__ == "__main__":
    print("Times:")
    for ts in times:
        m = re.match(time_regex, ts)
        status = " OK:" if m else " Bad:"
        print(status, ts)

    print("\nDurations:")
    for ds in durations:
        m = re.match(dur_regex, ds)
        status = " OK:" if m else " Bad:"
        print(status, ds)