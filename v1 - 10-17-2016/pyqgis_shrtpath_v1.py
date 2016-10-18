from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *
from qgis.networkanalysis import *

vl = qgis.utils.iface.mapCanvas().currentLayer()
director = QgsLineVectorLayerDirector( vl, -1, '', '', '', 3 )
properter = QgsDistanceArcProperter()
director.addProperter( properter )
crs = qgis.utils.iface.mapCanvas().mapRenderer().destinationCrs()
builder = QgsGraphBuilder( crs )

pStart = QgsPoint(235186.886, 895896.681)
pStop = QgsPoint(235321.803, 894311.402)

tiedPoints = director.makeGraph( builder, [ pStart, pStop ] )
graph = builder.graph()

tStart = tiedPoints[ 0 ]
tStop = tiedPoints[ 1 ]

idStart = graph.findVertex( tStart )
idStop = graph.findVertex( tStop )

( tree, cost ) = QgsGraphAnalyzer.dijkstra( graph, idStart, 0 )

if tree[ idStop ] == -1:
  print "Path not found"
else:
  p = []
  curPos = idStop
  while curPos != idStart:
    p.append( graph.vertex( graph.arc( tree[ curPos ] ).inVertex() ).point() )
    curPos = graph.arc( tree[ curPos ] ).outVertex();

  p.append( tStart )

  rb = QgsRubberBand( qgis.utils.iface.mapCanvas() )
  rb.setColor( Qt.red )

  for pnt in p:
    rb.addPoint(pnt)