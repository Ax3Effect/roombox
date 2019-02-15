# roombox
## Inspiration
The original idea for roombox came from a common frustration at parties - everyone loves Spotify, but why doesn't it allow other people to queue songs in a playlist? Eventually, we became fed up with constantly queueing songs for others, and decided to build roombox, a simple room-based queueing system for Spotify.

## What it does
roombox allows users to create password-protected rooms, which in turn creates a playlist in their Spotify account. Other people can then join that room and queue songs into that playlist - the idea being that Spotify plays through whatever has been queued in order, removing the need for someone to oversee the music.

## How we built it
For the backend, we used Flask - a powerful template-driven Python web framework designed with modularity and scalability in mind. This allowed us to build roombox up from just a home page without really needing to modify our existing code. This definitely made the development process go a little more smoothly, as well as providing a lot of useful inbuilt stuff.

For the frontend, we elected to use a framework called MaterializeCSS - this was perfect for a variety of reasons:

It allowed us to have a site which worked well on both mobile and desktop browsers.
It allowed us to create a site with a very clean, minimal design.
MaterializeCSS has toast notifications built in - we used a Flask template to effectively create a "message handler" for Flask messages, which let us create toast notifications using only Flask's inbuilt flash() function.
It removed a lot of the guesswork involved in creating a usable layout; most of the elements arrange themselves into a neat layout without much work on our part.
Challenges we ran into
Honestly, the development went quite smoothly all things considered. We ran into an issue where a bug in our code caused the database into an odd state, resulting in errors when performing queries - because we weren't storing any valuable data at that stage in development, we could work around the problem by deleting the database until we fixed the bug. In general, we found that database management was the most difficult part of the project to implement. Aside from that, there were no show-stopping issues, and we were able to get roombox finished relatively quickly.

## Accomplishments that we're proud of
The server is resource-efficient enough that it runs fairly quickly with memory to spare inside the cheapest available DigitalOcean droplet ($5/mo for 512MB RAM, 20GB SSD and 1 vCore). If we run into performance issues as time goes on, we may consider upgrading, but for now it works fine.
We were able to get the project finished in just over 12 hours - this left us plenty of time to squish any minor bugs and usability issues that we found with the project after that point.
What we learned
Developing roombox taught us a lot about front-end development more than anything; making sure the site was straightforward, ensuring the next steps were obvious, et cetera. We found that a lot of our time was spent rearranging things on the frontend to remove unnecessary steps, and fixing usability issues with the layout (like putting the search bar above the queue, where previously it was below and could end up off-screen). Additionally, it was nice to learn how the Spotify Web API works, and we learned a lot about how to make requests (and parse the response) using the popular requests library available on pip.

## What's next for roombox
We have thrown around the idea of preparing roombox for public use - the idea seems to be popular with people who have had it demonstrated to them, and the site is pretty close to being ready for public consumption - we just need to finish implementing little "polish" things (like auto playlist deletion after a given time, and the ability for the host to delete things from the queue).
