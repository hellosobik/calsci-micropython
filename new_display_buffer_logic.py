import os
# menu_buffer=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
text_buffer="Mechanical engineering designs, analyzes, and improves systems."
# text_buffer="nagesh"
menu_buffer_size=len(text_buffer)
menu_buffer=list(range(menu_buffer_size))
# menu_buffer=["angle", "fun", "consts", "equations", "search", "cloud", "wifi", "settings"]
menu_buffer_cursor=0
rows=3
cols=12
display_buffer_position=0
display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
no_last_spaces=0
while True:
    if len(text_buffer)%cols!=0:
        no_last_spaces=cols-len(text_buffer)%cols
        for i in range(0,cols-len(text_buffer)%cols):
            text_buffer+=" "
            menu_buffer_size=len(text_buffer)
            menu_buffer=list(range(menu_buffer_size))
    while len(text_buffer)<=display_buffer[-1] or len(text_buffer)<rows*cols:
        no_last_spaces+=1
        text_buffer+=" "
        menu_buffer_size=len(text_buffer)
        menu_buffer=list(range(menu_buffer_size))
    display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
    os.system('clear')
    counter=0
    for i in range(rows):
        print("")
        row=""
        for j in range(cols):
            if counter >= len(display_buffer):
                row+="\t"
            elif display_buffer[counter]==menu_buffer_cursor:
                row+="|"+str(text_buffer[display_buffer[counter]])
            else:
                row+="  "+str(text_buffer[display_buffer[counter]])
            counter+=1
        print(row)
    print("")
    text=input("Enter the text: ")
    if text=="d" or text =="r":
        if text=="d":
            menu_buffer_cursor+=cols
        else:
            menu_buffer_cursor+=1
        if menu_buffer_cursor >= len(menu_buffer)-no_last_spaces:
            menu_buffer_cursor=0
            display_buffer_position=0
        elif menu_buffer_cursor > display_buffer[-1]:
            display_buffer_position+=cols
    elif text=="u" or text=="l":
        if text=="u":
            menu_buffer_cursor-=cols
        else:
            menu_buffer_cursor-=1
        if menu_buffer_cursor < 0:
            menu_buffer_cursor=len(menu_buffer)-no_last_spaces-1
            display_buffer_position=len(menu_buffer)-rows*cols
        elif menu_buffer_cursor < display_buffer[0]:
            display_buffer_position-=cols
    elif text=="b":
        if menu_buffer_cursor < 0:
            menu_buffer_cursor=0
            display_buffer_position=0
        elif menu_buffer_cursor < display_buffer[0]:
            text_buffer=text_buffer[0:menu_buffer_cursor-1]+text_buffer[menu_buffer_cursor:len(text_buffer)]
            display_buffer_position-=cols
            menu_buffer_size=len(text_buffer)
            menu_buffer_cursor-=1
        elif menu_buffer_cursor > 0 and menu_buffer_cursor>=display_buffer[0]:
            text_buffer=text_buffer[0:menu_buffer_cursor-1]+text_buffer[menu_buffer_cursor:len(text_buffer)]
            menu_buffer_size=len(text_buffer)
            menu_buffer_cursor-=1
    else:
        text_buffer=text_buffer[0:menu_buffer_cursor]+text+text_buffer[menu_buffer_cursor:len(text_buffer)]
        menu_buffer_size+=len(text)
        menu_buffer=list(range(menu_buffer_size))
        menu_buffer_cursor+=len(text)
        if menu_buffer_cursor>display_buffer[-1]:
            display_buffer_position=menu_buffer_cursor-menu_buffer_cursor%cols-((rows-1)*cols)
    text_buffer=text_buffer.strip()+" "