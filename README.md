# Sea Dog Marine Website

Static, schema-rich local SEO site: 30 pages (home, 7 services, 3 county pages, service area hub, free inspection page, blog hub, 16 blog posts) plus sitemap.xml, robots.txt and llms.txt.

## Before launch (fill in build.py CONFIG, then run `python3 build.py`)
1. SITE_URL: the real domain. Every canonical, sitemap and schema URL comes from this.
2. HOURS: real hours. Must match Google and Apple listings exactly.
3. EMAIL and BASE_CITY: optional but recommended.
4. SAME_AS: Google Business Profile URL, Facebook, Instagram, Yelp, Nextdoor once they exist.
5. Swap the flyer crops in /assets for real job photos as soon as Shea has them (same file names). Real before and after photos with geotags help local rankings.

## Deploy (same stack as Island Applicators)
1. Push the `site/` folder to a GitHub repo.
2. DigitalOcean App Platform: Create App, pick the repo, type Static Site, output dir `/` (or `site` if you push the whole project).
3. Add the domain in DigitalOcean, point DNS, confirm HTTPS.
4. Google Search Console: add domain property, submit `https://DOMAIN/sitemap.xml`.
5. Bing Webmaster Tools: import from Search Console (feeds ChatGPT search and Copilot).

## Google Maps (Google Business Profile)
- Category: primary "Marine Cleaning Service" if available, otherwise closest match; add secondaries like "Pressure Washing Service" and "Marine Surveyor" only if accurate.
- Set as a service area business (hide address). Add Pinellas, Hillsborough and Manatee counties plus top cities.
- Name exactly "Sea Dog Marine". No keyword stuffing in the name (suspension risk).
- Phone 727-699-4920, website = home page, hours = same as site.
- Add every service from the site with the same names and short descriptions.
- Upload 20+ real photos: logo, before and after, crew, truck or boat, each job.
- Post weekly: share each blog post as a GBP update with a photo (16 weeks of content ready).
- Reviews: text every customer the review link right after the job. Reply to all reviews, mention the service and city naturally.
- Add the Q&A from the site FAQs.

## Apple Maps (Apple Business Connect: businessconnect.apple.com)
- Claim or create the place card with identical name, phone, hours, website and categories.
- Add logo, cover photo and Showcases (feature the free video inspection).
- Add the "Call" and "Website" action links.
- Apple pulls ratings from Yelp and its own ratings, so set up a Yelp page too.

## AI search optimization (ChatGPT, Gemini, Perplexity, Apple Intelligence, Google AI Overviews)
- Already built in: LocalBusiness, Service, FAQPage, BlogPosting and Breadcrumb schema on every page; a plain-language "What does Sea Dog Marine do?" answer block; robots.txt allowing AI crawlers; llms.txt summary.
- Keep name, phone and service area identical everywhere (site, GBP, Apple, Yelp, Facebook, Nextdoor, BBB).
- Get listed on Yelp, Nextdoor, Facebook, BBB, Angi and local chamber directories. AI answers lean on these third-party citations.
- Reviews that mention service + city ("seawall cleaning in Apollo Beach") are the strongest signal for both Maps and AI answers.
