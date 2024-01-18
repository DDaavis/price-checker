import customtkinter
import insertdb
import selectCategory
import graphWindow
import getprice
import deleteData
import messages

# UI izveide, izmantojot custom Tkinter
customtkinter.set_appearance_mode("light") # var mainīt uz 'light' un 'System'
customtkinter.set_default_color_theme("green") # man patika vēl 'green', bet tad ar redzamību švaki

# Galvenais UI:            
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Ja ir vēlme pievienot vēl veikalus, protams pie helpers.py ir jāzveido skripts kas meklēs cenu
        # Un jāievieto veikala nosaukums šeit - tam jābūt tieši tādam kā helpers.py get_price_from_X
        # Ja ir vēlme mainīt veikala nosaukumu šeit, tas pats jāzidara būs arī pie helpers.py :)

        availableShops = ["Choose a site", "dateks", "m79",
                            "1a", "rdveikals", "tet", "balticdata", "elkor"]
        
        # Ja pareizi atceros, tad šeit var pievienot un noņemt kategorijas pēc savas patikas
        availableCategories = ["Category", "CPU", "GPU", "RAM",
                                    "Motherboard", "Power Supply", "Memory", "Case", "CPU Cooler"]

        # šis ir paredzēts UI centrēšanai
        # window.eval('tk::PlaceWindow . center') neder, jo centrēs nevis visu logu, bet gan top-left stūri
        width = 1000 # izmērus pēc vajadzības brīvi var mainīt
        height = 550
        x = int((self.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.winfo_screenheight() / 2) - (height / 1.5))
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.title("Price Checker")
        self.expand = True

        # Scale ievietoju mainīgajā, lai programma automātiski pielāgotu citas vērtības kas ir atkarīgas no scale
        scale = 1.3 # Padarīs programmu lielāku vai mazāku (upscale, downscale)
        padx = 20
        customtkinter.set_widget_scaling(scale)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.minsize(width, height) # Lai lietotājs nevarētu izķēmot programmu, ievietoju minsize

        # Mainot scale vai padx automatiski aprēķinās platumu tā, lai 'tab' būtu centrā
        self.tabview = customtkinter.CTkTabview(self, width=width/scale-padx*2)
        self.tabview.grid(row=0, column=2, padx=(padx, padx), pady=(20, 0), sticky="nsew")
        self.tabview.add("Category")
        self.tabview.add("Add a Product")
        self.tabview.add("Delete a Product")
        self.tabview.tab("Category").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Add a Product").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Delete a Product").grid_columnconfigure(0, weight=1)
        # Pirmajai lapai tie dropdown menu
        self.produkts_izvele = customtkinter.CTkOptionMenu(self.tabview.tab("Category"), dynamic_resizing=True,
                                                        values=self.allProducts(), command = self.produkta_izvele_changed)
        self.produkts_izvele.grid(row=1, column=0, padx=(5,5), pady=(0, 10))

        self.cenu_iegusana_kategorija = customtkinter.CTkOptionMenu(self.tabview.tab("Category"), dynamic_resizing=True,
                                                        values=selectCategory.category_selection(), command = self.typeToProducts)
        self.cenu_iegusana_kategorija.grid(row=0, column=0, padx=(5,5), pady=(20, 10))

        self.veikals_pirma_lapa = customtkinter.CTkOptionMenu(self.tabview.tab("Category"), dynamic_resizing=True,
                                                        values=deleteData.get_product_shop(self.produkts_izvele.get()))
        self.veikals_pirma_lapa.grid(row=2, column = 0, padx=(20,20), pady=(0, 10))

        # Otrajai lapai 
        self.majaslapasIzvele = customtkinter.CTkOptionMenu(self.tabview.tab("Add a Product"), dynamic_resizing=True,
                                                        values=availableShops)
        self.majaslapasIzvele.grid(row=2, column=0, padx=(20,20), pady=(20, 10))
        self.produktaTips = customtkinter.CTkOptionMenu(self.tabview.tab("Add a Product"), dynamic_resizing=True,
                                                        values=availableCategories)
        self.produktaTips.grid(row=3, column=0, padx=(20,20), pady=(0, 10))

        self.productURL = customtkinter.CTkEntry(self.tabview.tab("Add a Product"), placeholder_text="URL")
        self.productURL.grid(row=1, column=0, columnspan=3, padx=(20, 20), pady=(5, 0), sticky="nsew")

        self.productName = customtkinter.CTkEntry(self.tabview.tab("Add a Product"), placeholder_text="Product Name")
        self.productName.grid(row=0, column=0, columnspan=1, padx=(20, 20), pady=(5, 0), sticky="nsew")

        self.uploadButton = customtkinter.CTkButton(self.tabview.tab("Add a Product"), text="Upload", command=self.dataValidation)
        self.uploadButton.grid(row=4, column=0, padx=(20,20), pady=10)

        # Šis atkal pirmajai lapai
        self.searchButton = customtkinter.CTkButton(self.tabview.tab("Category"), text = "Get Prices", command = self.getPrices)
        self.searchButton.grid(row=4, column=0, padx=(5,5), pady=(20,0))
        self.graphButton = customtkinter.CTkButton(self.tabview.tab("Category"), text = "Get Graph", command = self.getGraph)
        self.graphButton.grid(row=5, column=0, padx=(5,5), pady=(10,0))

        self.textbox = customtkinter.CTkTextbox(self.tabview.tab("Category"), width=width/2-padx*3, height = height/2-padx)
        self.textbox.grid(column=1, row = 0, rowspan = 6, padx=(5,5), pady=(20, 0), sticky="nsew")
        self.textbox.configure(state="normal", wrap = 'none')
        self.textbox.insert('1.0', "The 'Get Prices' button will make this useful :)")
        self.textbox.configure(state="disabled", wrap = 'none')

        # Šis trešajai lapai
        self.kategorijas_dzesanai = customtkinter.CTkOptionMenu(self.tabview.tab("Delete a Product"), dynamic_resizing=True,
                                                         values=selectCategory.category_selection(), command = self.product_type_changed)
        self.kategorijas_dzesanai.grid(row=0, column = 0, padx=(20,20), pady=(20, 10))

        self.produkts_dzesanai = customtkinter.CTkOptionMenu(self.tabview.tab("Delete a Product"), dynamic_resizing=True,
                                                        values=self.allProducts(), command = self.product_delete_changed) #command = self.check_delete_type)
        self.produkts_dzesanai.grid(row=1, column = 0, padx=(20,20), pady=(0, 10))

        self.veikals_dzesanai = customtkinter.CTkOptionMenu(self.tabview.tab("Delete a Product"), dynamic_resizing=True,
                                                        values=deleteData.get_product_shop(self.produkts_dzesanai.get()))
        self.veikals_dzesanai.grid(row=2, column = 0, padx=(20,20), pady=(0, 10))

        self.deleteButton = customtkinter.CTkButton(self.tabview.tab("Delete a Product"), text="Delete", command = self.delete_button_clicked)
        self.deleteButton.grid(row=4, column=0, padx=(20,20), pady=10)

    # Visas funkcijas kas nepieciešamas UI:
        
    # Nepieciešams, lai pārliecinātos, ka visi dati tika pareizi ievadīti 'Add a Product' tab-ā.
    def dataValidation(self):
        if (self.produktaTips.get() != 'Category' and self.majaslapasIzvele.get() != "Choose a site" 
            and self.productURL.get() != "" and self.productName != ""):

            insertdb.datu_ievietosana_kad_pievieno(self.productName.get(), self.produktaTips.get(), self.majaslapasIzvele.get(), self.productURL.get() )
            # print(self.produktaTips.get(), self.majaslapasIzvele.get(), self.productURL.get(), self.productName.get())
            # print("World!")

            self.produkts_izvele.configure(values = selectCategory.get_all_products())
            self.cenu_iegusana_kategorija.configure(values = selectCategory.category_selection())

            messages.product_uploaded()
            self.refreshFields()

        else:
            
            messages.wrong_input()

    # Balstoties uz atlasīto tipu, parādīs tipam piederošos produktus
    # Piemēram, ja izvēlēsies tipu 'CPU', option menu parādīs visus produktus kam tips ir 'CPU'
    def typeToProducts(self, something):

        if self.cenu_iegusana_kategorija.get() == 'Every Category':
            array = selectCategory.get_all_products()
            self.produkts_izvele.configure(values = array)
            self.produkts_izvele.set("Every Product")
            self.veikals_pirma_lapa.configure(values = [('Every Shop')])
            self.veikals_pirma_lapa.set('Every Shop')

        else:

            array = selectCategory.get_product_from_category(something)
            self.produkts_izvele.configure(values = array)
            self.produkts_izvele.set("Every Product")
            self.veikals_pirma_lapa.configure(values = [('Every Shop')])
            self.veikals_pirma_lapa.set('Every Shop')
    
    # Funkcija paredzēta, lai pareizi strādātu 'typeToProducts' funkcija
    def allProducts(self):
        array = selectCategory.get_all_products()
        return array
    
    # paredzēts, lai varētu iegūt datus no 'Add a Product' lapas option menus
    def get_data_from_dropdown(self):

        tips = self.cenu_iegusana_kategorija.get()
        produkts = self.produkts_izvele.get()
        veikals = self.veikals_pirma_lapa.get()

        # Ja netiek mainīts ne kategorija, ne produkts
        if tips == 'Every Category' and produkts == 'Every Product':
            
            dati = getprice.cenu_iegusana_visi_produkti()
            self.visualize(dati)
        # ja kaut viens no tiem tiek mainīts
        else:
            # Ja ir mainīts produkta nosaukums, ir nepieciešams tikai iegūt šo konkrēto produkta nosaukumu :)
            if produkts != 'Every Product' and veikals == 'Every Shop':
                dati = getprice.cenas_tikai_nosaukums((produkts))
                self.visualize(dati)
            # Ja ir mainīta kategorija, bet nav mainīts produkts, tad ir jāiegūst visi kategorijas produkti
            if tips != 'Every Category' and produkts == 'Every Product':
                dati = getprice.cenas_pec_tipa(tips)
                self.visualize(dati)
            # Ja ir mainīts tik sīki, ka izvēlēts ir pat veikals
            if produkts != 'Every Product' and veikals != 'Every Shop':
                dati = getprice.cenas_pec_nosaukuma_un_veikala(produkts, veikals)
                self.visualize(dati)
            

    # Parādīs datus uz ekrāna, kad tiks uzspiests 'Get Prices'
    def visualize(self, dati):
        # row[x]: 0 - produktsPK, 1 - tips, 2 - nosaukums
        # 3 - veikalsPK, 4 - veikala nosaukums, 5 - produkta_modelis, 6 - cena, 7 - url, 8 - date_checked
        self.textbox.configure(state="normal", wrap = 'none')
        self.textbox.delete(0.0, 'end') # iztīrīs textBox no visa vecā teksta
        self.textbox.configure(state="disabled", wrap = 'none')
        oldName = ''
        value = ''

        for rows in dati: # Šeit formulēts kā izskatīties datiem
            
            if oldName == rows[0]:
                value = '\n   Shop: ' + rows[1] + '\n   Price: ' + rows[2] +'\n   Date: ' + rows[4] + '\n   URL: ' + rows[3] + '\n\n'
                self.textbox.configure(state = "normal")
                self.textbox.insert("end", value)
                self.textbox.configure(state = "disabled")
                oldName = rows[0]

            else:
                value = rows[0] + '\n\n   ' + 'Shop: ' + rows[1] + '\n   Price: '+ rows[2] +'\n   Date: '+ rows[4]+ '\n   URL: ' + rows[3] + '\n\n'
                self.textbox.configure(state = "normal")
                self.textbox.insert("end", value)
                self.textbox.configure(state = "disabled")
                oldName = rows[0]
        
    # Funkcija uzrādīs visu produktu tagadējo cenu, veikalu, datumu, url
    def getPrices(self):
        self.get_data_from_dropdown()

    # Balstoties uz pilnīgi visiem datiem, tiks iegūta katra produkta cenas vēsture un izveidota diagramma
    # Diagramma tiks veidota atkarībā no tā kāds produkts(i) tiek izvēlēti
    def getGraph(self):

        tips = self.cenu_iegusana_kategorija.get()
        produkts = self.produkts_izvele.get()
        veikals = self.veikals_pirma_lapa.get()
        # tipsFormatets = '' + tips
        # produktsFormatets = '' + produkts
        graphWindow.buildGraph(tips, produkts, veikals)

    # Izmantoju, lai, ja lietotājs izvēlas produktu, automātiski tiek piešķirts produkta tips
    # def check_delete_type(self, produkts):

    #     tips = self.kategorijas_dzesanai.get()

    #     if produkts == 'Every Product' and tips != 'Every Category':
    #         self.kategorijas_dzesanai.set('Every Category')

    #     produktaTips = deleteData.get_product_type(produkts)

    #     if produkts != 'Every Product' and tips == 'Every Category':
    #         # jadabu produkta tips
    #         self.kategorijas_dzesanai.set(produktaTips)
    #         array = deleteData.get_product_shop(produkts)
    #         self.veikals_dzesanai.configure(values = array)

    def product_type_changed(self, category):

        self.produkts_dzesanai.configure(values = deleteData.get_product_from_type(category))
        self.produkts_dzesanai.set('Every Product')
        self.veikals_dzesanai.configure(values = (['Every Shop']))
        self.veikals_dzesanai.set('Every Shop')


    def product_delete_changed(self, produkts):

        array = deleteData.get_product_shop(produkts)

        if produkts == 'Every Product':

            self.veikals_dzesanai.set('Every Shop')
            self.veikals_dzesanai.configure(values = (['Every Shop']))
        else:
            self.veikals_dzesanai.set('Every Shop')
            self.veikals_dzesanai.configure(values = array)

    # Funkcija pildīs to, kas notiek, kad uzspiež pogu 'Delete'
    def delete_button_clicked(self):

        tips = self.kategorijas_dzesanai.get()
        produkts = self.produkts_dzesanai.get()
        veikals = self.veikals_dzesanai.get()
        deleteData.delete_selected_products(tips, produkts, veikals)
        messages.product_deleted()
        self.refreshFields()

    # Šis paredzēts laukumu atsvaidzināšanai
    def refreshFields(self):

        allCategories = selectCategory.category_selection()
        allProducts = self.allProducts()

        # Atjaunināšana pie delete page
        self.kategorijas_dzesanai.configure(values = allCategories)
        self.kategorijas_dzesanai.set('Every Category')
        self.produkts_dzesanai.configure(values = allProducts)
        self.produkts_dzesanai.set('Every Product')
        self.veikals_dzesanai.configure(values = (['Every Shop']))
        self.veikals_dzesanai.set('Every Shop')

        # Atjaunināšana pie get price un get graph page
        self.veikals_pirma_lapa.configure(values = (['Every Shop']))
        self.veikals_pirma_lapa.set('Every Shop')
        self.produkts_izvele.configure(values = allProducts)
        self.produkts_izvele.set("Every Product")
        self.cenu_iegusana_kategorija.configure(values=allCategories)
        self.cenu_iegusana_kategorija.set('Every Category')

    def produkta_izvele_changed(self, produkts):

        array = deleteData.get_product_shop(produkts)

        if produkts == 'Every Product':
            self.veikals_pirma_lapa.configure(values = (['Every Shop']))
            self.veikals_pirma_lapa.set('Every Shop')
        else:
            self.veikals_pirma_lapa.configure(values = array)
            self.veikals_pirma_lapa.set('Every Shop')

if __name__ == "__main__":
    app = App()
    app.mainloop()