import os

# menu_buffer=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
text_buffer="Mechanical engineering designs, analyzes, and improves systems."
menu_buffer_size=len(text_buffer)
menu_buffer=list(range(menu_buffer_size))
# menu_buffer=["angle", "fun", "consts", "equations", "search", "cloud", "wifi", "settings"]
menu_buffer_cursor=0
rows=5
cols=4
display_buffer_position=0
display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
# display_buffer_cursor=0
# menu_buffer_end=len(text_buffer)-1
no_last_spaces=0
while True:
    if len(text_buffer)%cols!=0:
        no_last_spaces=cols-len(text_buffer)%cols
        for i in range(0,cols-len(text_buffer)%cols):
            text_buffer+=" "
            menu_buffer_size=len(text_buffer)
            menu_buffer=list(range(menu_buffer_size))
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
                row+=" >"+str(text_buffer[display_buffer[counter]])
                # row+=" >"+str(text_buffer[counter])
            else:
                row+="  "+str(text_buffer[display_buffer[counter]])
                # row+="  "+str(text_buffer[counter])
            counter+=1
        print(row)


    print("")
    text=input("Enter the text: ")
    if text=="d":
        menu_buffer_cursor+=cols
        if menu_buffer_cursor >= len(menu_buffer):
            # menu_buffer_cursor=0
            # display_buffer_position=0
            # display_buffer_cursor=0

            # display_buffer_cursor=(menu_buffer_cursor-len(menu_buffer))%cols
            display_buffer_position=(menu_buffer_cursor-len(menu_buffer))//cols
            menu_buffer_cursor=menu_buffer_cursor-len(menu_buffer)

        # elif menu_buffer_cursor <= display_buffer[-1]:
        #     # display_buffer_cursor+=cols
        #     pass
        elif menu_buffer_cursor > display_buffer[-1]:
            display_buffer_position+=cols
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]

    elif text=="u":
        menu_buffer_cursor-=cols
        if menu_buffer_cursor <0:
            display_buffer_cursor=len(display_buffer)+menu_buffer_cursor
            menu_buffer_cursor=len(menu_buffer)+menu_buffer_cursor
            if menu_buffer_cursor>=len(menu_buffer)-no_last_spaces:
                menu_buffer_cursor=len(menu_buffer)-no_last_spaces-1
            # menu_buffer_cursor=len(menu_buffer)-1
            display_buffer_position=len(menu_buffer)-rows*cols
            # display_buffer_position=len(menu_buffer)%cols-(rows-1)*cols
            # display_buffer_position=len(menu_buffer)-len(menu_buffer)%(rows*cols)+cols-len(menu_buffer)%cols

        # elif menu_buffer_cursor >= display_buffer[0]:
        #     display_buffer_cursor-=cols
        elif menu_buffer_cursor < display_buffer[0]:
            display_buffer_position-=cols
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
    
    elif text=="r":
        menu_buffer_cursor+=1
        if menu_buffer_cursor>=len(menu_buffer)-no_last_spaces:
            # display_buffer_cursor=(menu_buffer_cursor-len(menu_buffer))%cols
            # display_buffer_position=(menu_buffer_cursor-len(menu_buffer))//cols
            display_buffer_position=0
            # menu_buffer_cursor=menu_buffer_cursor-len(menu_buffer)
            if menu_buffer_cursor>=len(menu_buffer)-no_last_spaces:
                menu_buffer_cursor=0
        elif menu_buffer_cursor>display_buffer[-1]:
            display_buffer_position+=cols
            # display_buffer_cursor
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]

    elif text=="l":
        menu_buffer_cursor-=1
        if menu_buffer_cursor<0:
            # display_buffer_cursor=len(display_buffer)+menu_buffer_cursor
            # menu_buffer_cursor=len(menu_buffer)+menu_buffer_cursor
            menu_buffer_cursor=len(menu_buffer)-no_last_spaces-1
            display_buffer_position=len(menu_buffer)-rows*cols
            # if menu_buffer_cursor>=len(menu_buffer)-no_last_spaces:
            #     menu_buffer_cursor=len(menu_buffer)-no_last_spaces-1
        elif menu_buffer_cursor<display_buffer[0]:
            display_buffer_position-=cols
            # display_buffer_cursor
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
    
    else:
        text_buffer=text_buffer[0:menu_buffer_cursor+1]+text+text_buffer[menu_buffer_cursor+1:len(text_buffer)]
        menu_buffer_size+=len(text)
        menu_buffer=list(range(menu_buffer_size))
        menu_buffer_cursor+=len(text)
        if menu_buffer_cursor>display_buffer[-1]:
            # display_buffer_position=((menu_buffer_cursor)//(rows*cols-1))*(rows*cols)
            display_buffer_position=menu_buffer_cursor-menu_buffer_cursor%cols-((rows-1)*cols)
        display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
    text_buffer=text_buffer.strip()

        


    
    #print(display_buffer, menu_buffer_cursor, display_buffer_cursor)

        
