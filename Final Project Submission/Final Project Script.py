#importing arcpy and setting workspace env. INPUT YOUR WORKSPACE HERE
import arcpy
arcpy.env.workspace = "C:\Users\romeo\Documents\Class\GEOG 380\Final Project"

#creating a variable for the map document. INPUT YOUR MAP DOC HERE
mxd = arcpy.mapping.MapDocument("CURRENT")

#listing dataframes
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

#insert your INPUT:Street Center Lines shp here
#creates shp variable and adds the Streets as a layer to mxd
Streetsshp = "GrandwoodParkRoads\GrandwoodParkRoads.shp"
Streets = arcpy.mapping.Layer(Streetsshp)
Streetsfc = arcpy.mapping.AddLayer(df,Streets,"TOP")

#generating points along every street, 200 ft apart. 
arcpy.GeneratePointsAlongLines_management("GrandwoodParkRoads", "Streetlights", "DISTANCE", "200 Feet", "", "")

#adding Streetlights as layer
streetlights = arcpy.mapping.Layer("Streetlights")
arcpy.mapping.AddLayer(df,streetlights,"TOP")

#Zooming to the Selected features (Streetlights)
expression = "'Shape' = 'Point'"
arcpy.SelectLayerByAttribute_management(streetlights,"NEW_SELECTION",expression)
df.extent = streetlights.getSelectedExtent()
arcpy.RefreshActiveView()

#Adjusting Legend Elements.
#Turning auto add on so that the streetlights and streets are added to legend.
#If contents of legend are overflowing, increase width by .1 pixel until it's not.
legend = arcpy.mapping.ListLayoutElements(mxd,"LEGEND_ELEMENT", "Legend")[0]
legend.autoAdd = True
while legend.isOverflowing:
	legend.elementWidth = legend.elementWidth + 0.1

#Saving a copy to results folder
#INPUT YOUR OWN FILE PATH
mxd.saveACopy(r"C:\Users\romeo\Documents\Class\GEOG 380\Final Project\results\\Grandwood Park Streetlights.mxd")

#Saving layout as PDF
#INPUT YOUR OWN FILE PATH 
arcpy.mapping.ExportToPDF(mxd, r"C:\Users\romeo\Documents\Class\GEOG 380\Final Project\results\Grandwood Park Streetlights.pdf")

