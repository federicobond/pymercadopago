import mercadopago

mp =  mercadopago.Client("8644045002109454", "Mh95YOKGlEHyiJ8D4YUQtagf29C1m2nF") 

mp.invoices.get("12345")
