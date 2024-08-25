#Demoonstration circuit for common current mirror

#standrad cell libraries
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.gf180_mapped  import gf180_mapped_pdk  as gf180
from glayout.flow.pdk.mappedpdk import MappedPDK


# Primitives
from glayout.flow.primitives.fet import pmos
from gdsfactory import Component
from glayout.flow.primitives.guardring import tapring

# Utilities
from glayout.flow.pdk.util.comp_utils import evaluate_bbox,prec_center

# Routing
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route

def currentMirror(pdk: MappedPDK):
    #Crate a top level componenet
    
    currentMirror = Component()
    #We want two pFETS
    pfet_ref = pmos(pdk, with_substrate_tap=False,with_dummy=(True,False))
    pfet_mir = pmos(pdk, with_substrate_tap=False,with_dummy=(False ,True))
    pfet_ref_ref = currentMirror << pfet_ref
    pfet_ref_mir = currentMirror << pfet_mir
    
    #relative Move
    #Move the second pFET to the right of the first pFET
    ref_dimentions = evaluate_bbox(pfet_ref)
    pfet_ref_mir.movex(ref_dimentions[0] + pdk.util_max_metal_seperation())
    
    #Rounting
    #Route the source and drain of the two pFETs
    currentMirror << straight_route(pdk,pfet_ref_ref.ports["multiplier_0_source_E"],pfet_ref_mir.ports["multiplier_0_source_W"] )

    currentMirror << straight_route(pdk,pfet_ref_ref.ports["multiplier_0_gate_E"],pfet_ref_mir.ports["multiplier_0_gate_W"] )
    
    currentMirror << c_route(pdk,pfet_ref_ref.ports["multiplier_0_drain_W"],pfet_ref_ref.ports["multiplier_0_gate_W"] )
    
    shift_amount = - prec_center(currentMirror.flatten())[0]
    tap_ring = tapring(pdk,enclosed_rectangle=evaluate_bbox(currentMirror.flatten(), padding=pdk.util_max_metal_seperation()))
    tr_ref= currentMirror << tap_ring
    
    tr_ref.movex(shift_amount)

    return currentMirror
    
    
    