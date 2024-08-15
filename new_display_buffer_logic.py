import os

menu_buffer=[0,1,2,3,4,5,6,7,8,9]
menu_buffer_cursor=0
rows=5
display_buffer_position=0
display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows]
display_buffer_cursor=0

while True:
    #global menu_buffer_cursor, menu_buffer, rows, display_buffer_position, display_buffer, display_buffer_cursor 
    #print(display_buffer, menu_buffer_cursor, display_buffer_cursor)
    os.system('clear')
    for i in display_buffer:
        row=""
        if i==menu_buffer_cursor:
            row+="> "+str(i)
        else:
            row+="  "+str(i)
        print(row)
    direction=input("Enter the direction: ")
    if direction=="d":
        menu_buffer_cursor+=1
        if menu_buffer_cursor == len(menu_buffer):
            menu_buffer_cursor=0
            display_buffer_position=0
            display_buffer_cursor=0
        elif menu_buffer_cursor <= display_buffer[-1]:
            display_buffer_cursor+=1
        elif menu_buffer_cursor >= display_buffer[-1]:
            display_buffer_position+=1
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows]

    elif direction=="u":
        menu_buffer_cursor-=1
        if menu_buffer_cursor <0:
            menu_buffer_cursor=len(menu_buffer)-1
            display_buffer_position=len(menu_buffer)-rows
            display_buffer_cursor=rows-1
        elif menu_buffer_cursor >= display_buffer[0]:
            display_buffer_cursor-=1
        elif menu_buffer_cursor <= display_buffer[0]:
            display_buffer_position-=1
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows]
    
    #print(display_buffer, menu_buffer_cursor, display_buffer_cursor)

        
