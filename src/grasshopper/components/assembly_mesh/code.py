__author__ = "petras"
__version__ = "2023.04.13"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs


import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
from Rhino.Geometry import BoundingBox
from Rhino.Geometry import Point3d
from Rhino.Geometry import Plane
from Rhino.Geometry import Polyline
from Rhino.Geometry import Vector3d
from Rhino.Geometry import Line
from Rhino.Geometry import TextEntity
from Rhino.Geometry import Transform
from System.Drawing import Color
import math

class MyComponent(component):
   
    bbox = BoundingBox.Unset
    lines = []
    insertion_vectors_current = []
    joint_per_face_current_text_entity = []
    meshes = []
    material = Rhino.Display.DisplayMaterial(Color.FromArgb(200, 200, 200))
    def DrawViewportWires(self, args):
        try:
            for o in self.meshes:
                #args.Display.DrawBrepWires(o, Color.FromArgb(0, 0, 0))
                args.Display.DrawMeshShaded(o, self.material)
                args.Display.DrawMeshWires(o, Color.Black,1)
            pass
            #            plane = Plane.WorldXY
            #            for line in self.lines:
            #                args.Display.DrawLineArrow(line, Color.FromArgb(207, 0, 90), 2, 100)
            #            for polyline in self.polylines:
            #                args.Display.DrawPolyline(polyline, Color.FromArgb(207, 0, 90), 2)
            #            for insertionVectorsCurrent in self.insertion_vectors_current:
            #                if(insertionVectorsCurrent.Length<0.05):
            #                    continue
            #                args.Display.DrawLine(insertionVectorsCurrent, Color.FromArgb(0, 0, 0), 5)
            #            for jointPerFaceCurrent in self.joint_per_face_current_text_entity:
            #                result, plane = Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.ActiveViewport.GetCameraFrame()
            #                plane.Origin=(jointPerFaceCurrent.Plane.Origin)
            #                args.Display.Draw3dText(jointPerFaceCurrent.PlainText, jointPerFaceCurrent.MaskColor, plane, jointPerFaceCurrent.TextHeight, "Arial", False, False,Rhino.DocObjects.TextHorizontalAlignment.Center, Rhino.DocObjects.TextVerticalAlignment.BottomOfTop)      
        except Exception, e:
            System.Windows.Forms.MessageBox.Show(str(e), "script error")
   
    def get_ClippingBox(self):
        return self.bbox
   
   
           
    def display_insersion_sequence(self, _meshes, _lines,_t):
       
        text_size = 50
        line_scale = 300
       
        ###############################################################################
        # input
        ###############################################################################
        self.bbox = BoundingBox.Unset
        self.lines =  _lines if len(_lines) > 0 else [Line(Point3d(0,0,0),Point3d(0,0,1))]
        self.insertion_vectors_current =  []
        self.joint_per_face_current_text_entity = []
        self.meshes =  []
        
        _n = 1
        group_count = _n if _n is not None else 1
        t = _t if _t is not None else 0.0
        item = self.lines[0]
        self.bbox = self.lines[0].BoundingBox
       
        ###############################################################################
        # process
        ###############################################################################
        for i in range(1,len(self.lines)) :
            self.bbox.Union(self.lines[i].BoundingBox)
       
        for i in range(0,int(math.floor(t)))  :
           self.meshes.append(_meshes[i])
       
        if (t % 1 > 0):
           
            id2 = int(math.floor(t))
            meshes_current = []
           
            for i in range(group_count):
                meshes_current.append(_meshes[id2])
           
            for m in range(len(meshes_current)) :
               
                item = self.lines[id2]
                line_from = item.From
                item = self.lines[id2]
                to = line_from - item.To
               
                mesh = meshes_current[m].Duplicate()
                mesh.Transform(Transform.Translation(to * (1 - t % 1)))
                meshes_current[m] = mesh
           
            for i in meshes_current:
                self.meshes.append(i)
           
        # return outputs if you have them here I try it for you:
        return #self.polylines
   
    def RunScript(self, _meshes, _dir,  _t):
        self.display_insersion_sequence(_meshes, _dir,_t)