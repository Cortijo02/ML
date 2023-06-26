import pandas

def handle_gpu(row):
    gpu = row["Gpu"].lower().strip()
    
    replacements = {
        "intel graphics 620": "intel hd graphics 620",
        "amd r4": "amd radeon r4",
        "nvidia geforce gtx1050 ti": "nvidia geforce gtx 1050 ti",
        "nvidia geforce gtx 1050ti": "nvidia geforce gtx 1050 ti",
        "nvidia geforce gtx1060": "nvidia geforce gtx 1060",
        "nvidia geforce gtx1080": "nvidia geforce gtx 1080",
        "nvidia geforce mx130": "nvidia geforce 130mx",
        "nvidia geforce mx150": "nvidia geforce 150mx",
        "nvidia geforce gt 940mx": "nvidia geforce 940mx",
        "nvidia gtx 980 sli": "nvidia geforce 980"
    }

    # Quitar unicode no valido
    if "<" in gpu:
        gpu = gpu[:-8]

    # Quitar graphics del final
    if gpu.startswith("amd") and gpu.endswith("graphics"):
        gpu = gpu[:-9]

    # Cambiar el nombre a otro mas normalizado
    if gpu in replacements:
        gpu = replacements[gpu]

    # Quitar gtx del nombre porque hay algunas que no lo tienen
    gpu = gpu.replace("gtx ", "")

    return gpu

def handle_cpu(row):
    cpu = row["Cpu"].lower().strip()

    replacements = {
        "amd e-series 6110 1.5ghz": "amd e2-series 6110 1.5ghz",
        "amd e-series 9000 2.2ghz": "amd e2-series 9000 2.2ghz",
        "amd a10-series a10-9620p 2.5ghz": "amd a10-series 9620p 2.5ghz",
        "amd a12-series 9720p 3.6ghz": "amd a12-series 9720p 2.7ghz", # Aparentemente son el mismo pero sin overclock
        "amd a6-series 9220 2.9ghz": "amd a6-series 9220 2.5ghz", # Misma razon
        "amd a6-series a6-9220 2.5ghz": "amd a6-series 9220 2.5ghz",
        "amd e-series 7110 1.8ghz": "amd e2-series 7110 1.8ghz",
        "amd e-series 9000e 1.5ghz": "amd e2-series 9000e 1.5ghz",
        "amd e-series e2-6110 1.5ghz": "amd e2-series 6110 1.5ghz",
        "amd e-series e2-9000 2.2ghz": "amd e2-series 9000 2.2ghz",
        "amd e-series e2-9000e 1.5ghz": "amd e2-series 9000e 1.5ghz",
        "amd a9-series a9-9420 3ghz": "amd a9-series 9420 3ghz",
        "amd a9-series 9420 2.9ghz": "amd a9-series 9420 3ghz",

        "intel celeron dual core n3350 2ghz": "intel celeron dual core n3350 1.1ghz",
        "intel celeron dual core n3350 2.0ghz": "intel celeron dual core n3350 1.1ghz",
        "intel celeron dual core n3060 1.60ghz": "intel celeron dual core n3060 1.6ghz",

        "intel core i3 6006u 2.2ghz": "intel core i3 6006u 2.0ghz",
        "intel core i3 6006u 2ghz": "intel core i3 6006u 2.0ghz",

        "intel core i3 6100u 2.1ghz": "intel core i3 6100u 2.3ghz",

        "intel core i5 7200u 2.70ghz": "intel core i5 7200u 2.5ghz",
        "intel core i5 7200u 2.7ghz": "intel core i5 7200u 2.5ghz",
        "intel core i5 7200u 2.50ghz": "intel core i5 7200u 2.5ghz",
        
        "intel core i7 6500u 2.50ghz": "intel core i7 6500u 2.5ghz",
        "intel core i7 7500u 2.5ghz": "intel core i7 7500u 2.7ghz",
        "intel core i7 7700hq 2.7ghz": "intel core i7 7700hq 2.8ghz",

        "intel core m 6y30 0.9ghz": "intel core m m3-6y30 0.9ghz",
        "intel core m 7y30 1.0ghz": "intel core m m3-7y30 2.2ghz",
        "intel core m 6y75 1.2ghz": "intel core m m7-6y75 1.2ghz",

        "intel atom z8350 1.92ghz": "intel atom x5-z8350 1.44ghz",

        #"intel a9 9420 2.9ghz": "intel a9 9420 3ghz"
    }

    if cpu in replacements:
        cpu = replacements[cpu]

    # Quitar -series
    if "amd" in cpu:
        cpu = cpu.replace("-series", "")

    return cpu

def handle_product(row):
    product = row["Product"].lower()

    if "(" in product:
        return product.split("(")[0]

    return product

import sys
def main():
    df = pandas.read_csv(sys.argv[1])

    df["Gpu"] = df.apply(lambda row: handle_gpu(row), axis=1)
    df["Cpu"] = df.apply(lambda row: handle_cpu(row), axis=1)
    df["Product"] = df.apply(lambda row: handle_product(row), axis=1)
    df["TypeName"] = [ x.lower() for x in df["TypeName"] ]
    df["ScreenResolution"] = [x.lower() for x in df["ScreenResolution"]]
    df["Memory"] = [x.lower() for x in df["Memory"]]
    df["Company"] = [x.lower() for x in df["Company"]]
    df["OpSys"] = [x.lower() for x in df["OpSys"]]
    df["Ram"] = [x.lower() for x in df["Ram"]]

    for _ in sorted(set(df["TypeName"])):
        print(_)

    print("len:", len(set(df["TypeName"])))

    if len(sys.argv) > 2:
        df.to_csv(sys.argv[2])

main()

