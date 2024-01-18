import matplotlib.pyplot as plt
from datetime import datetime
import graphData

# ([price, date_checked, produkta_nosaukums, veikals])
def buildGraph(tips, produkts, veikals):
    # Grafika lieluma maiņa
    width, height = 1000, 550
    plt.figure(figsize=(width / 100, height / 100)) # Pieņem tikai inches

    rows = graphData.get_data_for_graph(tips, produkts, veikals) # Iegūstu datus no DB
    all_product_data = {}

    for row in rows:

        priceToString = str(row[0]).replace(',', '.') # Ja kādā cenā gadās ',', jāpārveido uz '.'
        if priceToString != '-':
            price = float(priceToString) # šis arī ir iemesls kāpēc vajadzēja pārveidot uz '.'
        else: price = None
        nosaukums = row[2] + ' ' + row[3] # šis būs leģendām grafikā - produkta nosaukums + veikala nosaukums
        date_checked = row[1]
        # Ar milisekundēm un sekundēm izskatās pārpildīts, tāpēc tās izņemu, lai nerāda
        cr_date = datetime.strptime(date_checked, '%Y-%m-%d %H:%M:%S.%f').strftime("%m/%d/%Y %H:%M")

        if cr_date not in all_product_data:
            all_product_data[cr_date] = {}
        all_product_data[cr_date][nosaukums] = price

    # Leģendām iegūst unikālus produktu nosaukumus
    product_names = set(nosaukums for data in all_product_data.values() for nosaukums in data)
    # Kaut kāda iemesla dēļ krāsas līnijām nebija vienādas ar punktiem, tāpēc pievienoju šo
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Datu ievietošana diagrammā
    common_dates = sorted(all_product_data.keys(), key=lambda x: max(all_product_data[x].keys()))
    for i, nosaukums in enumerate(product_names):
        prices = [all_product_data[date].get(nosaukums, None) for date in common_dates]
        color = color_cycle[i % len(color_cycle)]  # Šis arī bija vajadzīgs, lai krāsas būtu normālas
        plt.plot(common_dates, prices, label=nosaukums, linestyle='-', marker='o', markersize=5, color=color)

    plt.ylabel("Price (Eur)")
    plt.xlabel("Date")
    plt.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')

    # Lai nebūtu pārtraukumi grafikā - ja produktam nav zināma cena konkrētā laikā, ielieku tam pēdējo zināmo cenu
    # Pirms nomainīju, ka laiku ņem tikai HH:MM, šis bija ļoti nepieciešams, jo katram produktam bija sava sekunde kad ieguva cenu.
    # Tagad iespēja, ka nesakritīs mazāka, bet plkst. nomainās minūte - datumi nesakritīs.
    for i, nosaukums in enumerate(product_names):
        prices = []
        last_known_value = None
        for date in common_dates:
            value = all_product_data[date].get(nosaukums, None)
            if value is not None:
                last_known_value = value
            prices.append(last_known_value)
        color = color_cycle[i % len(color_cycle)] 
        plt.plot(common_dates, prices, label=nosaukums, linestyle='-', linewidth=1, color=color)

    # Šis ir vajadzīgs, lai redzētu leģendas, bez šī vajadzīgs liela izmēra logs
    plt.subplots_adjust(right=0.75)
    plt.subplots_adjust(bottom=0.18)
    x_positions = [common_dates[i] for i in range(len(common_dates)) if i % 2 == 0] # parādīt tikai katru otro datumu
    plt.xticks(x_positions, rotation=25)
    plt.show()
