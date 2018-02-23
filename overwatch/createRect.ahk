#SingleInstance off

Box_Init(C="FF0000") {
  ; Added WS_EXTENDED_TRANSPARENT to make the overlay click-through
  Gui,+E0x20 +ToolWindow -Caption +AlwaysOnTop +LastFound
  ; Set window to 50% transparency
  WinSet,Transparent,64
  Gui,Color, % C
}

; Box_Draw - Draws a box on the screen using 4 GUIs.
; X - The X coord.
; Y - The Y coord.
; W - The width of the box.
; H - The height of the box.
Box_Draw(X, Y, W, H, O="I") {
  ; No longer adding to the height since using only a single rectangle
  If(W < 0)
    X += W, W *= -1
  If(H < 0)
    Y += H, H *= -1
  ; Removed the options and calculation for the border (T and O) since it no
  ; longer applies. Now the drawing dimensions are completely straight-forward.
  Gui, Show, % "x" X " y" Y " w" W " h" H " NA"
}

; Box_Destroy - Destoyes the 4 GUIs.
Box_Destroy() {
  Gui,Destroy
}

; Box_Hide - Hides the GUI.
Box_Hide() {
  Gui,Hide
}

Box_Init("00FF00")



p1 = % A_Index + 1
p2 = % A_Index + 2
p3 = % A_Index + 3
p4 = % A_Index + 4
param1 = %p1%
param2 = %p2%
param3 = %p3%
param4 = %p4%
;DllCall("mouse_event", uint, 1, int, %param1%, int, %param2%)



Box_Draw(%p1%, %p2%, %p3%, %p4%)
sleep, 100
Box_Destroy()
exitApp