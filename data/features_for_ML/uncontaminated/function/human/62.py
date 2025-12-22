def get_voltages(shotn):
        outdict = {}
        for attk in att_dict:
            tinner = att_dict[attk]
            try:
                if tinner["PS"]:
                    taa_v = client.get("XCM/" + tinner["name"] + "/VOLTS", shotn)
                else:
                    taa_v = client.get("XCM/" + tinner["name"] + "/VOUT", shotn)
                outdict[attk] = {
                    "data": taa_v.data,
                    "times": taa_v.time.data,
                    "units": taa_v.units,
                }
            except:
                pass  # print('voltages not found for coil '+attk+', shot '+str(shotn))
        return outdict