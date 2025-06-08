---
title: "GERTY from 'Moon'"
author: "@JumpSushi, @laij6, @GenericVillain37"
description: "A Recreation of 'GERTY' from the film 'Moon'"
created_at: "2025-06-05"
---
# June 5th, 2025 JumpSushi

Mainly worked on the BOM and parts hunting, and as I've done many of these kinds of projects before with speakers and boost convertors, I chose some that I've used before. IP2312 for battery chraging mainly because it can supply up to 3A, instead of the commonly used TPS4056 (1A).

As for the Pi, I chose a Pi 3, as that's what I had laying around, and should be decently powerful for the task of playing some music and showing some pictures of smiley faces.

For battery, I went with a 20000mAh battery, (two 10000mAh cells stacked together in parallel), which should give around ~10 Hours batt life assuming power draw of 2A, (pretty much worst case scenario).

Two 5V Boost convertors used, just to even out the load a bit. (the ic identification on the boards have been scratched off, but it worked fine in previous applications).

For the small light from gerty near the top, I chose a WS2812B LED Lightstrip, as that's probably the cheapest and most common option for something like this.

The camera is an offbrand raspberry pi camera module, therefore its decently cheap and should work fine.

Here's a quick wiring diagram I drew up:

![Wiring Diagram](https://hc-cdn.hel1.your-objectstorage.com/s/v3/f04d3f518c8f41d2216c4ae72a73d32464367516_screenshot_2025-06-08_at_8.21.11___pm.png)

I know it's pretty much illegible, I'll create a better one online.

Time taken: 1.5 Hours



# June 5th, 2025 GenericVillain37
Today I began designing the main body for the robot. It is painful. I have a reference image, but the proportions are odd, and we need to work out how the Pi and camera are going to fit in before I finish those holes. The sizing for the camera module took me a good few minutes, but I think it works. I had the image up on my iPad so I could see it better.

# June 5th, 2025 laij6
Today i started working on the bottom bit of the robot, this is the area underneath the main body, which generic villan is working on. After double checking the design about 20 minutes later, i realized some of the pieces were not the correct sizing as the part is meant to go inwards, and the panel meant to go above it had only been designed to the height instead of the length of the surface.

I needed to re-do some of the sizing on pieces meant to be put onto diagonal surfaces since they were to short and would just leave open areas at the top or bottom. When designing the bottom area, me and generic villain (the 2 body designers of this project) didn't communicate too well and had the scaling wrong. I compared the scaling of my design to his and both the short and long sections were 20mm too short.

The reference screenshots we took from the movie did not show the proportions too well or had ban lighting, making it hard to view. This hindered my designing speed quite a bit as i needed to create good props from scratch for the parts. Since the scaling between both mine and generic villans were different i needed to change some parts my design to the right scaling.

Because of this i also needed to change the sizing of other pieces connecting onto this to help create a balance within the design, I figured it would look weird if everything was completely proportioned wrong. This managed to be a pain as i pretty much had to redesign my whole section to fit the scaling of his. Communication errors, how great!

I beilieve that the sizing should match up well for these two pieces to connect together well and hopefully correctly. To be hounest, a lot of the time spent on this section was deciding the sizing of every part since we didnt have set lenghs for every part. Re doing the whole thing really didnt help with time conservation.

To help get the designing part done, i decided to make a design sheet without the correct proportions (just to get my ideas somewhere first) before actually creating the propper designs with the correct scalings and proportions.

![Planning sheet for design, this image contains the designs of the bottom area but this sheet is just for planning so none of this is scaled correctly yet](https://hc-cdn.hel1.your-objectstorage.com/s/v3/303c9cfb57215923347846b62333bf198c1940cd_img_0757.jpg)

Planning sheet for design, this image contains the designs of the bottom area but this sheet is just for planning so none of this is scaled correctly yet

![Final design with proper scaling for the smaller section](https://hc-cdn.hel1.your-objectstorage.com/s/v3/c0e0af28592d3473bdd0376148fa8f558397328f_img_0759.jpg)

Final design with proper scaling for the smaller section

![Final design with proper scaling for the longer section](https://hc-cdn.hel1.your-objectstorage.com/s/v3/7402a96cb6ebd93e01f7eb74835c36c1828c9571_img_0758.jpg)

Final design with proper scaling for the longer section

**Total time spent: 3h 20m**

# June 6th, 2025 laij6:
Similar to yesterday, my main focus is still on the bottom half of this project while the generic villain is working on the top area. Today, I worked on the legs of this robot as well as some add-ons for the left side of the robot. After a discussion with generic villain, we decided on most of the proportions of this project, which mostly included the proportions of already designed bits so that they would connect up well. In my opinion, this helped us overall combine our design, as now the proportions from the two designs match up. 

At the start of today, I started to work on the cupholder, which is meant to be put on the side of the robot. I first started with the top diameter of the semicircle at around 150mm. After I and generic villan started to compare design proportions and thinking about the sidebar, which I would design right after, we both thought that the cup holder was way too big, so the diameter of the circular area was shortened to 100mm. This also meant that the amount it was sticking out was shortened for proportional purposes, as usual. 

After this, I moved on to designing the sidebar, which is connected to the cup holder, also on the side of the robot, right behind it. When designing this, I had a slight misunderstanding with the design, thinking that the sidebar was sticking out farther than the cup holder, but after a quick look at a clip from the film, I realized my mistake. The side bar was meant to stick out around two-thirds as much as the cup holder did. This was a major time waster for me as I needed to redesign some bits of the sidebar because the proportion had been way off due to the change. I needed to cut the length, it was sticking out by half. 

After finishing the sidebar, I began to work on the legs, or more specifically, the smaller one first. the designing process for this was an absolute pain possibly even more so than the bigger leg, purely because of the amount of re dsigning i needed to do throughout this process. at first, i needed to come up with my measurements for the legs and getting measurements which would proportion properly to the rest of the body while not looking weird took longer than expected. 

At first, the design I made for the bottom of the small leg was a V shape with a longer edge on the front compared to the back. After this, I had moved onto the hands, which were mostly two rectangular prisms stacked onto each other, with two of these on a small surface. I had issues proportioning this to rectangles while still fitting well into the small surface area without being too thin, I ended up just making these squares (which I would soon change after completely redesigning this leg again). When designing plates to go onto these surfaces, just like in the main bottom area, I forgot about the fact that diagonals are longer than verticals, meaning I needed to redesign the plates. Another redesign because of sloppiness. 

after "finishing" this leg i looked at the refrence images as i was going to move onto the big leg then i realized how instead of the bottom of this leg being a v shape it was a diagonal connected to a bottom surface (similar to this: _/) meaning that i needed to redesign the bottom area. In this process, I also realized how off the lengths were compared to the rest of the body size, so I completely deleted the current progress and just restarted. I designed the legs to fit the one shown in the movie, and because of this, the overall size increased by about 15%. This helped with the hands mentioned earlier, as the wanted rectangular design wouldn't work well because of a lack of space. Now that the size has increased, meaning the surface area on which the hands are meant to be on increased, the rectangular design is now applicable. After this, I just needed to make simple changes to the surface plate's designs to finish up this leg. 

After finishing up the small leg, I moved on to designing the bigger one, which will prove to be just as painful and time-consuming to design. To start this leg, I began with the upper section before moving to the lower part. This area was annoying to make because the proportioning of it in the film was not very clear, and it was not shown too well in the film. Reference images also didn't prove too helpful with proportioning to the rest of the body, but did help me get the general shape of this bit. To be honest, the hardest part of the long leg was to find the proportions of the leg. After my first design of this leg, I found that some surfaces were too small compared to the other leg, so I needed to bump up the size by around 20% in some areas. I also found that the angles on certain areas were too subtle compared to the rest of the leg design, so I needed to start the angle off at six-eighths of the front leg length instead of my intended five-sixths. Because of the number of diagonals on this design, I needed to use a lot of double-to-triple decimal lines, which are more tedious to design with. This was especially apparent when making the plates for this leg as I had to constantly check the length of lines, which I found pretty tedious to do for every box.

![Final design for cup holder (10mm diameter)](https://hc-cdn.hel1.your-objectstorage.com/s/v3/0f5875a687ee1e3ddbe382495f91d652d95fa57e_cup_holder___side_notch.png)

Final design with proper scaling for the cup holder (10mm diameter on circular section)

![Final design for side bar](https://hc-cdn.hel1.your-objectstorage.com/s/v3/d6b1e72f4b658dfdf1daaa0e5a8011122c88ab80_side_bar.png)

Final design with correct proportioning for the sidebar

![Final design for small leg](https://hc-cdn.hel1.your-objectstorage.com/s/v3/d71c3be679726c5d9b7c756bca5e020c7f225432_small_leg.png)

Final design for the small leg 

![Final design for big leg](https://hc-cdn.hel1.your-objectstorage.com/s/v3/ea16cd5b586b2cbc1da6b9981482664a1cc360eb_big_leg.png)

Final design for big leg 

**Total time spent: 5h**


# June 7th, 2025 GenericVillain37:
During corespondence with Laij6, I realised that the notches on the top of my front-face were too small --- half the required size. I have spent a bit fixing that as well as designing the cover for the screen. Honestly, it was quite an average procces; no actual issues but it still took a while. 

**Time so far: 2hrs**

========

# June 7th, 2025 laij6:
Today, compared to previous days had a lot less work which i needed to get done. for today's designing activites i just started off by double checking the parts which i already designinged. and yes for more pain of redesigning i realized when comparing the hands to refrence images that the vertical lengh for the base rectangle was too short. previously i designed it thinking that i would leave around 5 or 10 cm on both above and below the rectangle so i had designined the hands with this in mind. and now after looking at the refrence images frmo the movie, this included the pain of low PPI when zooming into frames (bad lighting in many scenes also didnt really help with this). i saw that instead of there being empty space above and below the hands that it simply took up the full space. because of this i redesigned the hands to fully take the up space provided vertically (50mm). this didnt change the proportioning too much so i left the width the same. while look at the refrence screenshot i used for the hand redesign, i also saw that there is a bar around the top of the big leg meaning that i had another component to design. this was a reasonably quick process as there wasnt too much work to do that was alocated to me for this day. 

![resizing change of the hands and the added on piece](https://hc-cdn.hel1.your-objectstorage.com/s/v3/4f8a3f5e516e97cbd57f842b0e01283bea70799c_big_leg_add-ons.png)

This is the design for the hand sizing redesign along with the added piece.

**Total time spent: 45m**

# June 8th, 2025 GenericVillain37:

I spent a while trying to get the cupholder design of laij6 --- no no avail; I may add. I looked at the 100 most common food and beverages sold in the United States, which turned out to be the 100 most common food and beverages sold in the United States along with the 100 most common food and bevaages sold in the United States (the odd text in raw 3vs files), before finally figuring out how to download it. I discovered that there was, in fact, no peg on it (the thing I needed the dimensions for in order to design the hole on the side piece I have to make). I spent a couple seconds chiding my friend before getting on and adding it. I was editing laij6's side box when I realised I had not added the holes onto my own design for the front board. I proceeded to discover that I had underestimated the size of the screen and therefore had wasted at least an hour yesterday on designing the cover for the screen. I fixed this in a similar, boring fashion to the day before. Note: it is currently 2:58AM and so I shall be going to bed shortly. Expect further updates.

**Time so far: 3hrs**

Happy Second June 8th! I woke up this morining at roughly 9:00 (six hours of sleep) before going downstairs for breakfast. (Very design-orientated diary here I know). After that, I started immediatley on design. I uploaded some files from last night before getting to the side board. I began designing but soon realised that it needed to be longer to accomodate the side bar (which I had tried to work on the night before but was unfortunately prevented by the strange alignment to the grid). 

![design with peg](https://i.ibb.co/M4JjB1C/Mywork8-GERTY20250608.png)

Cup holder design but with the added peg

# June 8th, 2025 laij6:
So well, today was the absolute opposite of yesterday. So this morning, over a text chat with generic villan we had slight communication issues earlier on, and I thought that he was also working on designing the giant piece on the right of Gerty when looking front on, and found out he wasn't. Because we had nobody working on that major section, I decided to create that bit, and generic villan offered to create the part where he is held up by something and the connecting area to it, so I am leaving that to him. communication issues part inf! So to start today off, I began on the smallest piece of this design, which is the rectangular piece with slight add-ons on the top corners, which connects to Gerty directly. This part went pretty smoothly, to be honest, with only changes to the corners at the end. This small change included increasing the corner size, as I figured that when compared to the rest of the body, 10mm was slightly too thin, so I changed it to 20mm. This part didn't take too long, so I thought that this MIGHT not take a while. I am heavily mistaken (foreshadowing). So, after this, I moved on to a simpler, more straightforward piece, which was the box-like thing directly on top of it. This part, though having an easy shape, was a pain to design so that it proportions well compared to the rest of the body, and primarily the piece which was just designed, meaning the thing it is placed directly on. I took quite a while deciding the sizing ratio of the height compared to the top and bottom flat lengths, along with how far out the most left piece would be. I went through many sizing ratios (i.e., 1:2, 3:5, 2:3, etc). I eventually decided on a 1:3 ratio, which I found was most similar and simple compared to the reference images. I had to change the sizing on some of the side pieces that attach onto it to compensate for the height of the thing it is to be placed on. Most of the time I spent on this part was on the sizing. Lastly, I made the large part that connects to the back of all of this. As people say, "save the best for last," or, well, in my case, the most painful and time-consuming, to get the ratios of this piece, I used a ruler against my screen and compared it to the part I already designed with the height. With the result I got, I got 54 parts for the side which would be touching the box piece, 14 parts for the section above it, and 11 parts for the section below it. when comparing it to what i already made, I ended up with 4mm per part so i just multiplied every part by 4 and used that as my starter measurements. from here on out i only had refrence images which i had pulled up on my phone (this didnt help with the PPI and accuracy of the images) to create measurements for proportions. When creating proportions for this part, I mostly used fourths, eighths, or tenths as I find them the easiest to work around while still being reasonably accurate. This part was pretty simple with the angles and height comparison with the two sides, so just like the previous part, most of the time spent designing the face was on the proportioning. The process, which I thought would be the easiest section of creating one of these parts, ended up being the most time-consuming and tedious. For each side, I create a piece that makes it stick out from the main body, or pretty, making it like a box. This face ended up having 25 mostly unique sides, meaning that I had to create 25 singular pieces, which is easy to make but is extremely tedious. Most of the time spent on this design was on proportioning part faces or just creating the side pieces for it. That pretty much sums up what I ended up doing today.

![all three parts that I designed](https://hc-cdn.hel1.your-objectstorage.com/s/v3/9944a47b9b52483ad2b9a0af5946f92cc17ff358_frount_right_all_3_pieces.png)

design for all three of the side parts.

**Total time spent: 4h 30m**

