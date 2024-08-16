import os

# menu_buffer=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
menu_buffer=list(range(60))
# menu_buffer=["angle", "fun", "consts", "equations", "search", "cloud", "wifi", "settings"]
menu_buffer_cursor=5
rows=5
cols=6
display_buffer_position=0
display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
display_buffer_cursor=0

while True:
    #global menu_buffer_cursor, menu_buffer, rows, display_buffer_position, display_buffer, display_buffer_cursor 
    #print(display_buffer, menu_buffer_cursor, display_buffer_cursor)
    os.system('clear')
    # for i in display_buffer:
    #     row=""
    #     if i==menu_buffer_cursor:
    #         row+="> "+str(i)
    #     else:
    #         row+="  "+str(i)
    #     print(row)
    counter=0
    for i in range(rows):
        print("")
        row=""
        for j in range(cols):
            if counter >= len(display_buffer):
                row+="\t"
            elif display_buffer[counter]==menu_buffer_cursor:
                row+="\t> "+str(display_buffer[counter])
            else:
                row+="\t"+str(display_buffer[counter])
            counter+=1
        print(row)


    print("")
    direction=input("Enter the direction: ")
    if direction=="d":
        menu_buffer_cursor+=cols
        if menu_buffer_cursor >= len(menu_buffer):
            # menu_buffer_cursor=0
            # display_buffer_position=0
            # display_buffer_cursor=0

            display_buffer_cursor=(menu_buffer_cursor-len(menu_buffer))%cols
            display_buffer_position=(menu_buffer_cursor-len(menu_buffer))//cols
            menu_buffer_cursor=menu_buffer_cursor-len(menu_buffer)

        # elif menu_buffer_cursor <= display_buffer[-1]:
        #     # display_buffer_cursor+=cols
        #     pass
        elif menu_buffer_cursor > display_buffer[-1]:
            display_buffer_position+=cols
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]

    elif direction=="u":
        menu_buffer_cursor-=cols
        if menu_buffer_cursor <0:
            display_buffer_cursor=len(display_buffer)+menu_buffer_cursor
            menu_buffer_cursor=len(menu_buffer)+menu_buffer_cursor
            display_buffer_position=len(menu_buffer)-rows*cols
        # elif menu_buffer_cursor >= display_buffer[0]:
        #     display_buffer_cursor-=cols
        elif menu_buffer_cursor < display_buffer[0]:
            display_buffer_position-=cols
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
    
    elif direction=="r":
        menu_buffer_cursor+=1
        if menu_buffer_cursor>=len(menu_buffer):
            display_buffer_cursor=(menu_buffer_cursor-len(menu_buffer))%cols
            display_buffer_position=(menu_buffer_cursor-len(menu_buffer))//cols
            menu_buffer_cursor=menu_buffer_cursor-len(menu_buffer)
        elif menu_buffer_cursor>display_buffer[-1]:
            display_buffer_position+=cols
            # display_buffer_cursor
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]

    elif direction=="l":
        menu_buffer_cursor-=1
        if menu_buffer_cursor<0:
            display_buffer_cursor=len(display_buffer)+menu_buffer_cursor
            menu_buffer_cursor=len(menu_buffer)+menu_buffer_cursor
            display_buffer_position=len(menu_buffer)-rows*cols
        elif menu_buffer_cursor<display_buffer[0]:
            display_buffer_position-=cols
            # display_buffer_cursor
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
        


    
    #print(display_buffer, menu_buffer_cursor, display_buffer_cursor)

        
