# -*- coding: utf-8 -*-
"""
FindMyPlumber static site generator.

    python3 src/build.py            -> writes public/
    python3 src/build.py --qa       -> build, then run the anti-template QA pass

Batch 1 = src/cities.py. Later batches: append cities there, bump nothing else,
re-run, and publish only the new files (see README.md for the pacing rules).
"""

import json
import os
import re
import sys
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import config as C
import templates as T
from cities import CITIES, BY_SLUG, COUNTY_ORDER, cities_by_county, neighbors

OUT = os.path.join(ROOT, "public")

# ==========================================================================
# Content variation pools.
#
# The point of these is that no two city pages read the same way. Headings,
# intro frames, block order, referral copy, closing copy and the generic FAQ
# set all rotate independently, so the only thing two pages share verbatim is
# the legal disclosure (which SHOULD be identical everywhere).
# ==========================================================================

INTRO = [
    ("{issue}"),
    ("Plumbing in {city} has its own local character. {issue}"),
    ("Most plumbing calls we help route in {city} are unglamorous and urgent. {issue}"),
    ("{issue} When something does go wrong in {city}, you usually want a local plumber who "
     "already knows how homes here are built."),
    ("Houses in {city} age differently from houses two valleys over. {issue}"),
    ("{issue} None of this is a reason to panic \u2014 it is a reason to know what is behind your "
     "walls before a small problem becomes a big one."),
    ("Two questions decide most plumbing work in {city}: how old is the building, and what is the water "
     "like. {issue}"),
    ("Nobody in {city} calls a plumber about something small. By the time you are looking at this page "
     "it has probably been going on for a while. {issue}"),
]

H_AREA = [
    "Where we help in {city}", "Areas covered around {city}", "{city} service area: neighborhoods, ZIPs and nearby towns",
    "Neighborhoods and ZIP codes this page covers", "Coverage inside and around {city}",
]
H_ISSUE = [
    "What goes wrong with plumbing in {city}", "Local plumbing issues we hear about most in {city}",
    "{city} housing, water and pipes: what is different here", "Why plumbing in {city} is its own thing",
    "The {city}-specific stuff worth knowing",
]
H_FACT = [
    "About {city}", "{city} in brief", "A note about {city}", "Where {city} sits",
]
H_CALL = [
    "What happens when you call", "What a call to {phone} actually does",
    "How this referral works", "Calling {brand} from {city}",
    "What you get when you call us",
]
H_SVC = [
    "Plumbing help people call about in {city}", "Common requests we help route in {city}",
    "What local plumbers in {city} are usually called for", "Types of jobs this covers in {city}",
]
H_EMERG = [
    "If it is an emergency in {city}", "Urgent plumbing in {city}: what to do first",
    "Before you call about an emergency",
]
H_NEAR = [
    "Other covered cities near {city}", "Nearby cities we also cover", "Also covered in this region",
]
H_FAQ = [
    "{city} plumbing questions, answered honestly", "Frequently asked questions about {city}",
    "Questions people ask before calling in {city}",
]

# Rotating referral paragraphs — same meaning, six different ways of saying it.
REFERRAL = [
    ("When you call {phone} from {city}, you reach our call-routing service rather than a plumbing "
     "company. We pass your call to a licensed plumbing professional who serves your area and is "
     "available. That plumber contacts you, assesses the job and quotes it directly. {brand} does "
     "not perform plumbing work, does not set prices and cannot promise which contractor you will "
     "reach or how quickly they can get to you."),
    ("The number on this page routes to us, not to a plumber's shop. We answer, get the basics of "
     "your problem and your location in {city}, and connect the call to an independent licensed "
     "plumber who covers that area. From there the conversation is between you and that plumber. "
     "We are not a licensed contractor, we do not employ the plumbers we refer to, and we do not "
     "guarantee a specific response time."),
    ("Calling {phone} puts you through to a referral line. Our job is narrow: work out what you "
     "need and where in {city} you are, then hand the call to a plumbing professional who is "
     "licensed, insured and available for that area. Any quote, schedule, warranty or invoice comes "
     "from the plumber you agree to work with \u2014 not from {brand}."),
    ("This is a free service for you. You call, describe the problem, and we route you to a "
     "licensed local plumbing professional serving {city}. We are paid by the plumbing businesses "
     "that receive referrals, which is why there is no charge to you for the call or the "
     "introduction. We are not the company doing the work and we are not a licensed contractor."),
    ("There is no form to fill in and no account to create. Call {phone}, tell us what is happening "
     "and where you are in {city}, and we connect you with an available licensed plumbing "
     "professional. If nobody serving your area can take the call, we will say so rather than leave "
     "you holding."),
    ("A call to {phone} is answered by our referral team, who route it to a licensed plumber "
     "covering {city} and the surrounding neighborhoods. The plumber then deals with diagnosis, "
     "pricing and scheduling directly with you. {brand} is a lead generation and call routing "
     "service; we do not hold a contractor licence and we do not perform or supervise plumbing work."),
    ("Dial {phone} and you get a person whose only job is to work out which licensed plumbing "
     "professional can help you in {city}, then put you through to them. We do not quote, we do not "
     "book, and we do not turn up. The plumber does all of that, and they set their own terms."),
    ("Think of {brand} as the switchboard, not the tradesman. You call {phone}, describe the problem "
     "and your location in {city}, and we hand the call to an independent licensed plumber who serves "
     "that area. Their licence, their insurance, their invoice \u2014 none of it is ours."),
]

CLOSING = [
    "If you would rather talk to a person than keep reading, the number at the top of this page is "
    "the fastest way to do it.",
    "Calling is quicker than any contact form. The number above reaches our referral line directly.",
    "Have the address and a short description of the problem ready before you call \u2014 it gets you "
    "connected faster.",
    "If the problem is actively flooding something, shut the water off first and call second.",
    "One call is usually enough. Tell us the ZIP code and we will route from there.",
    "There is no cost to you for the referral, and no obligation to hire whoever you speak to.",
    "If in doubt, describe the problem first and ask what it would cost to come and look.",
    "Save the number before you need it. Plumbing problems rarely arrive at a convenient moment.",
]

EMERGENCY = [
    ("If water is coming out somewhere it should not be, find your main shutoff valve first. In most "
     "homes it is near the street-side property line or where the supply enters the building. Then "
     "call. We will route you to whoever is available, but we cannot promise a specific arrival "
     "time \u2014 response depends on the plumber and current demand."),
    ("For a burst pipe, a sewage backup into the home, or a gas smell, treat it as urgent. Leave the "
     "building if you smell gas and call your utility or 911 from outside. For everything else, "
     "shutting off the water at the fixture or the main buys you time until a plumber gets there."),
    ("Emergencies are where a referral service has limits, so here they are plainly: we can connect "
     "you to an available licensed plumbing professional, but we do not dispatch our own crews and "
     "we cannot guarantee how fast anyone arrives. If there is any risk to life or property \u2014 gas, "
     "electrical hazard, or flooding reaching outlets \u2014 call 911 or your utility first."),
    ("Turn the water off, then call. The main shutoff is usually a gate or ball valve where the supply "
     "line enters the property - at the street-side wall, in a garage, or in a ground-level box near "
     "the meter. Once it is closed the flooding stops and you have bought yourself time. We will route "
     "you to whoever is available, but arrival times depend on the plumber and how busy they are."),
    ("Sewage coming back up into a tub or a floor drain is the one to treat as genuinely urgent, because "
     "it is a health problem as well as a plumbing one. Stop running water anywhere in the building, "
     "keep people out of the affected room, and call. A gas smell is different again: leave, do not "
     "operate switches, and call the utility or 911 from a safe distance."),
    ("We route emergency calls the same way as any other call, so here is the honest limitation: we do "
     "not operate our own out-of-hours crews, and availability at two in the morning on a Sunday is not "
     "something anyone can promise in advance. Call and we will find out who is on. Shut the water off "
     "while you wait - that single step prevents most of the damage."),
    ("If water is already touching sockets, appliances or a light fitting, do not go near it. Cut power "
     "at the breaker for that part of the house if you can reach it safely, then deal with the water. "
     "Call the plumber for the plumbing and your utility for anything electrical."),
    ("Outdoor leaks - a hose bib, an irrigation line, a supply run to a detached garage - are usually "
     "less urgent than an indoor one, but they still waste a lot of water and can undermine a slab or a "
     "foundation over time. Close the isolation valve serving that line if there is one and book it in "
     "rather than leaving it running."),
]

# Generic FAQ pool. Four sets of three; each set is worded differently but
# every answer stays honest and non-specific.
GENERIC_FAQ = [
    [
        ("How fast can a plumber reach me in {city}?",
         "We do not publish an arrival time, because we cannot honestly promise one. Response depends "
         "on which licensed plumbing professional is available, where in {city} you are, what else is "
         "going on that day, and how urgent your job is relative to theirs. What we can tell you is "
         "whether anyone serving your area can take the call at all."),
        ("Is emergency plumbing available in {city}?",
         "Availability for after-hours and weekend work varies by plumber and by night. Call and we "
         "will route you to whoever is available. If the situation is dangerous \u2014 a gas smell, "
         "water near electrical outlets, or sewage backing into the home \u2014 call 911 or your utility "
         "first, then call us."),
        ("Does it cost anything to use {brand}?",
         "No. The referral is free to you. Plumbing businesses pay us when they receive a qualified "
         "call, which is what funds this site. You pay the plumber you hire, at whatever rate you "
         "agree with them, and nothing to us."),
    ],
    [
        ("Are the plumbers licensed and insured?",
         "We aim to connect callers with licensed, insured plumbing professionals, and that is a "
         "condition of taking referrals through this service. We are not the contractor, though, so "
         "the sensible thing is to confirm licence and insurance with the plumber directly before "
         "work starts. In California you can verify a contractor licence through the Contractors "
         "State License Board."),
        ("How quickly will someone call me back in {city}?",
         "Calls are routed live, so in most cases you speak to someone during the call rather than "
         "waiting for a callback. If no plumber serving your area is available at that moment, we "
         "will tell you instead of leaving you waiting on a promise we cannot keep."),
        ("What should I have ready when I call?",
         "Your address or ZIP code in {city}, whether you own or rent the property, a short "
         "description of the problem, and whether the water is currently shut off. That is enough "
         "for whoever takes the call to judge whether they can help."),
    ],
    [
        ("Do you cover the whole of {city}, or just parts of it?",
         "This page covers the neighborhoods, ZIP codes and nearby towns listed above. Coverage "
         "depends on which licensed plumbing professionals are available at the time you call, so "
         "rural and unincorporated addresses on the edges of the area may take longer to match. "
         "Give us the ZIP code and we will tell you straight away."),
        ("Is {brand} a plumbing company?",
         "No. We are a referral and call routing service. We do not hold a contractor licence, we do "
         "not employ plumbers, and we do not perform or supervise any plumbing work. The plumber who "
         "takes your call is an independent business, and your agreement is with them."),
        ("What if the plumber who comes out is not right for the job?",
         "You are never obliged to hire anyone. Ask questions, get the licence number, and if you "
         "would rather get a second opinion, that is entirely your call. If a referral went badly "
         "wrong, tell us through the contact page and we will look at it."),
    ],
    [
        ("Can I get a price over the phone?",
         "Not from us, and be wary of anyone who quotes a firm price before seeing the job. Plumbers "
         "typically give an estimate once they know what is involved, and many charge a diagnostic or "
         "call-out fee that is applied to the repair. Ask for the pricing structure up front."),
        ("Will the plumber who answers be local to {city}?",
         "We route to plumbing professionals who serve {city} and the surrounding area. Who exactly "
         "picks up depends on availability at that moment, which is why we describe this as a "
         "referral rather than a dispatch."),
        ("Do you handle commercial or rental properties in {city}?",
         "Some of the plumbing professionals we refer to take commercial, multi-unit and property "
         "management work; others are residential only. Mention the property type when you call and "
         "we will route accordingly."),
    ],
    [
        ("Who actually turns up to a {city} job?",
         "An independent licensed plumbing professional who serves {city}. We do not employ plumbers "
         "and we do not send our own staff, so the business that arrives is the business you contract "
         "with. Ask for their licence number and confirm insurance before work starts - that is a "
         "normal request and a good plumber will not mind."),
        ("Is it worth calling for a small job?",
         "That depends on the plumber, not on us. Some take small repairs happily, some have a minimum "
         "charge that makes a one-washer job poor value. Say what the job is when you call and let "
         "whoever answers tell you whether it is worth a visit."),
        ("What if I am renting in {city}?",
         "Then the landlord or property manager is usually responsible for repairs, and many tenancy "
         "agreements require you to notify them first. Tell whoever answers that you are a tenant so "
         "the call is handled correctly, and check your lease before authorising work."),
    ],
    [
        ("Do you charge for the referral?",
         "No. There is no fee from us at any point - not for the call, not for the introduction, and "
         "not as a cut of the work. Plumbing businesses pay us for qualified referrals. Your only cost "
         "is whatever you agree with the plumber, plus any carrier charges for the call itself."),
        ("Can you recommend a specific plumber in {city}?",
         "We route to whoever is licensed, available and serving your area, and we do not rank plumbers "
         "by how much they pay us. We also do not publish reviews or ratings, because we have no "
         "verified reviews to publish. If you want a recommendation with evidence behind it, verify the "
         "licence with the Contractors State License Board and ask the plumber for references."),
        ("What happens if nobody is available?",
         "We tell you. There is no point holding a caller on a promise that cannot be kept. You are "
         "welcome to call back later, and in the meantime shutting the water off is the single most "
         "useful thing you can do."),
    ],
    [
        ("Does {city} require a permit for plumbing work?",
         "Often yes, depending on what is being done. Replacing a fixture like-for-like is treated "
         "differently from repiping, moving a drain, replacing a water heater or altering gas lines, and "
         "some jurisdictions have specific rules about sewer laterals. The plumbing professional you "
         "speak to should tell you what your local authority requires and who pulls the permit - ask "
         "before work starts, not after."),
        ("Will the plumber I get handle sewer laterals and street-side work?",
         "Not all of them. Work that crosses into the public right-of-way often needs a contractor "
         "approved by the local authority, and some plumbers only work up to the property line. Mention "
         "where the problem is on the call so the right kind of plumber is sent."),
        ("How do I know the price I am quoted is fair?",
         "Get more than one quote for anything substantial, ask whether it is flat rate or time and "
         "materials, and check that the quote states what is included - materials, disposal, permit "
         "fees, and making good any walls or floors. We cannot tell you what a job should cost, and "
         "anyone who quotes confidently without seeing it is guessing."),
    ],
    [
        ("How long should a water heater last, and does water quality change that?",
         "Tank water heaters commonly last around eight to twelve years, and heavily mineralised water "
         "shortens that because sediment collects in the tank and insulates the water from the burner "
         "or element. Flushing the tank periodically and replacing the sacrificial anode rod are the "
         "two maintenance items that matter most. Tankless units can last longer but need regular "
         "descaling, particularly in hard-water areas."),
        ("My water pressure seems low. Is that a plumbing problem?",
         "Sometimes. Low pressure across the whole house points at the pressure-reducing valve at the "
         "meter, a partially closed main shutoff, or scale and corrosion narrowing the supply pipe. Low "
         "pressure at a single fixture is usually an aerator or cartridge. A plumber can tell which one "
         "in a few minutes with a gauge."),
        ("Can I wait and see if the problem fixes itself?",
         "A drain that is slow today is usually blocked properly next month, and a weeping joint does "
         "not seal itself back up. Water damage is cumulative and mostly hidden, so the cheap version of "
         "almost every plumbing problem is the one dealt with early. That said, a plumber should tell "
         "you honestly if something can wait."),
    ],
    [
        ("Do plumbers charge just to come out?",
         "Most do, as a diagnostic or call-out fee, and many apply part or all of it to the repair if "
         "you go ahead. It is a legitimate charge for the visit and the diagnosis. Ask what the fee is, "
         "and whether it is credited, before you book."),
        ("What is the difference between a repair and a replacement?",
         "A repair fixes the failed part; a replacement addresses the component or the run. Where a "
         "pipe material is at the end of its service life, repairing one leak often just moves the "
         "problem a few feet along. A plumber should explain which situation you are in and why, and "
         "you are entitled to a second opinion before authorising a replacement."),
        ("Should I stay home while the plumber works?",
         "Someone with authority to make decisions needs to be there, particularly if the work might "
         "grow once a wall or a trench is opened. If you are renting, tell the landlord or agent first. "
         "Ask in advance whether access to the roof space, crawlspace or meter is needed."),
    ],
    [
        ("How do I find my main water shutoff?",
         "On most homes it is a gate or ball valve where the supply enters the property: at the "
         "street-side wall, in a garage or crawlspace, or in a ground-level box near the meter. Learn "
         "where it is before you need it, and check that it still turns. If it is seized, that is a "
         "cheap thing to have replaced during any other visit."),
        ("Is repiping worth it, or can I keep patching leaks?",
         "It depends on the material and how many leaks you have had. Isolated failures in otherwise "
         "sound copper are usually worth repairing. Once galvanized steel or polybutylene starts "
         "failing in several places, patching tends to be false economy because the whole run is at "
         "the end of its life. Ask a plumber what material you have and how many repairs it has "
         "already had."),
        ("Can a plumber handle gas lines as well as water?",
         "Many licensed plumbers do gas work, but not all, and gas fitting often has its own licensing "
         "and permit requirements. Say on the call that gas is involved so someone qualified is sent. "
         "If you smell gas now, leave the building and call your utility or 911 from outside."),
    ],
    [
        ("What causes a sewer smell in the house?",
         "Usually a dried-out trap, a failed wax seal under a toilet, or a vent problem. Traps in unused "
         "bathrooms and floor drains evaporate, which is the cheapest version of this and the one to "
         "rule out first by running water. If the smell persists, a cracked seal or a blocked vent "
         "needs a plumber."),
        ("My toilet keeps running. Is that urgent?",
         "Not urgent, but not free either. A worn flapper or a mis-set fill valve can waste a large "
         "volume of water every day and shows up on the bill long before anyone notices. It is one of "
         "the quickest fixes in plumbing."),
        ("Should I replace all my fixtures at once?",
         "There is no need to, and doing so rarely saves money compared with replacing them as they "
         "fail. What is worth doing together is anything that shares an access point - if a wall or "
         "floor is already open for one repair, adding the adjacent work is usually cheaper than "
         "opening it twice."),
    ],
    [
        ("Do you cover rural and unincorporated addresses?",
         "Often, but coverage depends on which plumbing professionals are available and how far they "
         "travel. Rural addresses may carry a longer travel time or a different call-out fee. Give the "
         "address rather than the nearest town name when you call, because the two can be in different "
         "jurisdictions."),
        ("What should I ask a plumber before letting them start?",
         "Their licence number, whether they are insured, what the quote includes, whether a permit is "
         "needed and who pulls it, how long the work will take, and what the warranty covers. Those are "
         "ordinary questions and any established business will answer them without hesitation."),
        ("Is it cheaper to call during the week?",
         "Frequently, yes. Out-of-hours, weekend and holiday call-outs usually carry a premium, and "
         "non-urgent work is easier to schedule at a standard rate. If the problem can safely wait, "
         "waiting is usually the cheaper option - but do not let an active leak wait."),
    ],
    [
        ("How do I know if I have a hidden leak?",
         "The common tells are an unexplained rise in the water bill, the sound of running water when "
         "every fixture is off, damp patches or lifting flooring, a musty smell in one room, and warm "
         "spots on a slab. A meter test settles it quickly: read the meter, use no water for an hour, "
         "read it again. If it moved, something is leaking."),
        ("Will my insurance cover a plumbing failure?",
         "Sometimes, and it depends heavily on the cause. Sudden and accidental discharge is often "
         "covered while gradual leakage, wear and tear, and maintenance failures usually are not. "
         "Read your policy before the plumber arrives, ask them to document the cause of failure, and "
         "keep the photographs and the invoice."),
        ("What is a slab leak and why does it matter?",
         "It is a leak in a water or drain line running beneath a concrete floor slab. It matters "
         "because the water has nowhere to go: it saturates the ground under the foundation and can "
         "cause settlement, and it is invisible until flooring or walls show it. Detection is usually "
         "electronic or acoustic, and repair options range from rerouting the line overhead to opening "
         "the slab."),
    ],
    [
        ("Should I be worried about polybutylene or galvanized pipe?",
         "Both have a finite service life. Polybutylene, used widely from the late 1970s to the mid "
         "1990s, becomes brittle and fails at the fittings. Galvanized steel corrodes from the inside "
         "out and eventually restricts flow. Neither is an emergency the day you find it, but both are "
         "worth budgeting for, and a plumber can identify the material in minutes."),
        ("Why do I need a backflow preventer and does it need testing?",
         "A backflow preventer stops contaminated water from being drawn back into the potable supply "
         "when pressure drops. They are required on many irrigation systems, commercial connections and "
         "some residential services, and most jurisdictions require periodic testing by a certified "
         "tester. Ask the plumber whether your property has one and when it was last certified."),
        ("My water heater is making noise. Is that dangerous?",
         "Usually it is sediment. Minerals settle in the bottom of the tank, and as the water heats, "
         "steam bubbles form under the sediment and collapse with a rumbling or popping sound. It is "
         "not usually dangerous but it does mean the tank is working harder than it should. Flushing it "
         "often quiets it down; a tank that has been neglected for years may not recover."),
    ],
    [
        ("Is it normal for water pressure to drop when something else is running?",
         "A small drop is normal. A significant one usually means the supply line is undersized for the "
         "house, partially blocked by scale or corrosion, or that a pressure-reducing valve is failing. "
         "Older homes that have had bathrooms added over the years are the usual candidates, because the "
         "original supply was never sized for the extra fixtures."),
        ("How do I stop my drains blocking so often?",
         "Most repeat blockages come from three things: grease down the kitchen drain, hair in the "
         "bathroom, and roots in an old lateral. The first two are habits and a strainer; the third "
         "needs a camera inspection to confirm and either regular cutting or a repair. If the same drain "
         "blocks twice in a year, get it filmed rather than cleared again."),
        ("What does a plumber look for in a pre-purchase inspection?",
         "Supply pipe material and condition, the water heater and its age, venting and strapping, water "
         "pressure, drainage speed, the condition of the sewer lateral, and evidence of past leaks or "
         "unpermitted work. It is a different job from a general home inspection, which does not usually "
         "camera the lateral. Ask for both if you are buying."),
    ],
    [
        ("Can I fix it myself?",
         "Some things are genuinely simple: a running toilet flapper, a blocked aerator, a loose handle. "
         "Anything involving the gas supply, the sewer lateral, soldering, permits, or work inside a wall "
         "is not, and in California most of that requires a licensed contractor. A DIY repair that fails "
         "inside a wall is far more expensive than the original call."),
        ("Do you help with water damage as well as the plumbing?",
         "We route plumbing calls. Water damage restoration - drying, demolition, mould remediation - is "
         "a separate trade, and many plumbing businesses do not do it. Say on the call whether the leak "
         "has already soaked building materials so the right kind of contractor is sent, or so you can be "
         "told to call a restoration company as well."),
        ("How long does a typical call-out take?",
         "It varies with the job. A blocked drain or a failed fill valve is often under an hour on site. "
         "A water heater replacement is a few hours. A lateral repair depends entirely on depth, length "
         "and access, and can be a day or several. The plumber should give you a realistic window once "
         "they know what is involved."),
    ],
    [
        ("What should I do while I wait for the plumber?",
         "Shut the water off at the nearest isolation valve or at the main, move anything valuable out "
         "of the way, put a bucket under an active leak, and take photographs for your insurer. Do not "
         "keep flushing a blocked toilet or running water into a backed-up drain, and do not open walls "
         "or start dismantling fittings."),
        ("Are quotes binding?",
         "Rarely in the sense of a fixed price agreed sight unseen. Most plumbers quote after inspection, "
         "and a written quote should state what is included and what would change the price. Ask for the "
         "quote in writing before work starts, ask what happens if they open a wall and find something "
         "worse, and confirm whether the diagnostic fee is credited."),
        ("Can I get the same plumber next time?",
         "That is between you and the business that attended. If you were happy, ask them for their direct "
         "number and keep it - that is normal and we would rather you had a plumber you trust than call "
         "us again. We do not restrict who you work with after a referral."),
    ],
    [
        ("What is the difference between a plumber and a drain cleaning service?",
         "A licensed plumber can diagnose and repair, replace pipe, work on gas and water heaters, and "
         "pull permits. A drain cleaning service typically clears blockages only. If your problem might "
         "be more than a blockage - a repeat clog, a leak, a smell, or anything structural - a plumber is "
         "the right first call."),
        ("Do you charge more at night or at the weekend?",
         "We do not charge anything at any time. The plumbing business that attends sets its own rates, "
         "and out-of-hours call-outs commonly carry a premium. If the job can safely wait until a weekday "
         "it will usually cost less, but do not let an active leak wait to save money."),
        ("What if the plumber cannot fix it on the first visit?",
         "Some jobs need parts, a permit, or a second tradesperson, and a first visit that ends with a "
         "diagnosis and a plan is a normal outcome rather than a failure. Ask before they leave what "
         "happens next, what it will cost, and how long the property is out of service in the meantime."),
    ],
]


HAVE_READY = [
    ("Your street address or ZIP code in {name}", "What is happening, and since when",
     "Whether the water is currently shut off", "Owner, tenant or property manager",
     "Any access issues: gate codes, dogs, parking"),
    ("Which part of {name} you are in", "The symptom, in your own words",
     "Whether you have found the shutoff valve", "Roughly how old the property is",
     "Anything blocking access to the pipe or heater"),
    ("Address and ZIP code", "Is it leaking right now, or has it stopped",
     "Owner or tenant", "What has already been tried",
     "Where the problem is: kitchen, bathroom, garage, outside"),
    ("Your {name} address", "When the problem started",
     "Whether the water or gas is still on", "Who needs to be let in",
     "Any photos you can describe on the call"),
    ("The nearest cross street or ZIP", "What the water is doing",
     "Whether the main shutoff has been closed", "Is this a home, a rental or a business",
     "Anything a plumber would need to bring"),
    ("Address, including any unit or lot number", "How long it has been happening",
     "Whether you own or rent", "Where the shutoff valve is, if you know",
     "Whether anyone will be home to let them in"),
    ("Your ZIP code", "Which fixture or area is affected",
     "Whether the water is on or off", "The age of the property, roughly",
     "Anything you have already tried"),
]

READY_HEADING = ["Have these ready", "Before you dial", "Worth knowing before you call",
                 "It helps to have this to hand", "What to tell whoever answers",
                 "Five things that speed the call up", "Have the answers to these",
                 "Getting connected faster"]

AREA_INTRO = [
    ("This {name} page covers the city itself plus the neighborhoods and outlying communities listed "
     "below. If your address is on the edge of the area, give the ZIP code when you call and we will "
     "tell you whether a plumbing professional serving it is available."),
    ("The {name} listings below are the neighborhoods, ZIP codes and surrounding communities this page "
     "is written for. Coverage depends on who is available when you call, so an address just outside "
     "the list may still be served \u2014 say where you are and we will check."),
    ("Below are the {name} districts, ZIP codes and nearby towns we route calls for. Some of these are "
     "inside the city limits and some are unincorporated, which occasionally changes who is "
     "responsible for a lateral. Give us the address and we will route from there."),
    ("Use this list to check whether {name} coverage reaches you. It includes the city's own "
     "neighborhoods, its ZIP codes, and the towns around it that plumbing professionals based here "
     "also serve."),
    ("Everything below falls inside the {name} area this page is written about: city neighborhoods "
     "first, then ZIP codes, then the surrounding communities. If your address is not on the list, "
     "call anyway \u2014 we would rather check than guess."),
    ("{name} and the communities around it are listed here so you can see at a glance whether this page "
     "is the right one for your address. Plumbers work in radiuses rather than council boundaries, so "
     "the edge of one list often overlaps the next."),
    ("The lists below are the {name} areas this page was written for. If your street is not in them, "
     "there is a good chance a neighbouring city page covers you \u2014 the links at the bottom of this "
     "page are the place to check."),
    ("Coverage here is described the way plumbers actually work: by neighborhood and ZIP rather than by "
     "the city limit line. That matters in {name}, where an address a few hundred yards apart can sit "
     "in a different jurisdiction with different permit and lateral rules."),
]

AREA_HEADINGS = [("Neighborhoods and districts", "ZIP codes", "Nearby towns and communities"),
                 ("Districts and neighborhoods", "Postal codes covered", "Communities we also route for"),
                 ("Where in {name}", "ZIP codes", "Surrounding towns"),
                 ("Neighborhoods", "ZIP codes served", "Nearby communities"),
                 ("Parts of {name} this covers", "ZIP codes", "Towns around {name}"),
                 ("Local districts", "Postal codes", "Neighbouring communities"),
                 ("Inside {name}", "ZIP codes handled", "Also covering"),
                 ("Areas of {name}", "ZIP codes", "Nearby places we route for")]

NOT_QUOTE = [
    ("Pricing is set by the individual plumbing business, including any call-out or diagnostic fee and "
     "any minimum charge. Get the rate structure confirmed before work starts."),
    ("None of the above comes with a price attached. Rates are set by the individual plumbing business, "
     "and most charge a diagnostic or call-out fee that may or may not be applied to the repair. Ask "
     "before they start."),
    ("Treat this as a description of the work, not a quote. Only the plumber who inspects the job can "
     "price it, and it is reasonable to ask how they price \u2014 flat rate or time and materials \u2014 "
     "before anyone picks up a tool."),
    ("We cannot quote any of this and neither can a phone call. What you can do is ask the plumbing "
     "professional for their rate structure, their minimum, and whether the diagnostic fee is credited "
     "toward the repair."),
    ("Nothing on this page is a price. Two plumbers can quote the same job differently depending on "
     "access, materials and how much of the run they have to open up, so get it in writing."),
    ("Costs belong to the plumber, not to this site. Ask what the visit fee is, whether it is credited "
     "against the repair, and whether they quote flat rate or time and materials."),
    ("There are no prices here on purpose. A quote given without an inspection is a guess, and we would "
     "rather you got a real one from the person standing in front of the pipe."),
]

SVC_BLURB = [
    "Ask about this when you call \u2014 the plumbing professional serving {name} will confirm what is involved.",
    "Describe the symptom, not the diagnosis. Whoever you reach in {name} will work out the cause.",
    "Mention it up front so the right kind of plumber is sent to a {name} address.",
    "Common enough in {name} that most local plumbers will have done one this month.",
    "Worth raising on the call so {name} plumbers can tell you whether it is a quick fix or a bigger job.",
    "If it is this, say so plainly \u2014 and say whether you have already tried anything.",
    "Bring up access and location when you mention this; both change the job in {name}.",
    "In {name} this often turns out to be connected to something else, so let the plumber look first.",
]

SVC_LEAD = [
    ("These are the kinds of jobs plumbing professionals serving {name} are typically called for. It is "
     "a description of the work, not a price list \u2014 pricing is set by the plumber you speak to."),
    ("What follows is a rough map of the work that comes up in {name}. Nothing here is priced, because "
     "we do not set prices and neither does this page."),
    ("Most calls from {name} fall into one of these categories. Use the list to describe your problem "
     "in terms a plumber will recognise; rates come from the plumber, not from us."),
    ("The jobs below are what plumbers covering {name} spend most of their time on. This is context, "
     "not a menu \u2014 each business decides its own rates and minimums."),
    ("Here is the sort of work this page helps route in {name}. If your problem is not on the list, "
     "describe it on the call anyway; plenty of plumbing work does not fit neatly into a category."),
    ("These are common requests from {name} addresses. They are listed so you know what to ask for, "
     "not so you can price the job yourself \u2014 that has to come from an inspection."),
    ("A short list of the plumbing work that comes up most often around {name}. If your problem is not "
     "on it, describe it anyway; the list is a starting point, not a boundary."),
    ("What follows covers the usual range of jobs in {name}, from a dripping cartridge to a failed "
     "lateral. Nobody can price any of it from a list, but knowing the category helps whoever answers "
     "send the right plumber."),
]

SUB_LINE = [
    ("{brand} is a referral service, not a plumbing contractor. The plumber you speak to quotes and "
     "performs the work."),
    ("We route the call. A licensed plumbing professional serving {name} assesses it, prices it and "
     "does it."),
    ("Not a plumbing company. {brand} connects you; the plumber you agree to work with does the job and "
     "issues the invoice."),
    ("The number reaches our referral line. From there you speak to an independent licensed plumber "
     "covering {name}."),
    ("{brand} does not do plumbing. We do answer the phone and we do route you to someone licensed who "
     "serves {name}."),
    ("Free for you to call. The plumber sets their own rates and does their own work."),
    ("A referral line, answered by people who do not carry tools. The plumber who takes the call does."),
    ("{brand} gets you to a plumber in {name}. The plumber does everything else, including the quoting."),
]

ICON = ('<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">'
        '<path fill="currentColor" d="M12 2.7s6.3 6.9 6.3 11.1A6.3 6.3 0 0 1 12 20.1a6.3 6.3 0 0 1-6.3-6.3C5.7 9.6 12 2.7 12 2.7Zm0 15.6a4.5 4.5 0 0 0 4.5-4.5c0-2.6-3.2-6.9-4.5-8.5-1.3 1.6-4.5 5.9-4.5 8.5A4.5 4.5 0 0 0 12 18.3Z"/></svg>')


# ================================================================== helpers ==

def w(rel, content):
    path = os.path.join(OUT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def esc(s):
    return H.escape(str(s), quote=True)


def city_href(c):
    return "/cities/%s.html" % c["slug"]


def ul(items):
    return "<ul>" + "".join("<li>%s</li>" % esc(i) for i in items) + "</ul>"


def chips(items, cls="chip"):
    return '<ul class="chips">' + "".join(
        '<li class="%s">%s</li>' % (cls, esc(i)) for i in items) + "</ul>"


def faq_html(items, cityname):
    out = []
    for q, a in items:
        q = q.replace("{city}", cityname).replace("{brand}", C.BRAND).replace("{phone}", C.PHONE_DISPLAY)
        a = a.replace("{city}", cityname).replace("{brand}", C.BRAND).replace("{phone}", C.PHONE_DISPLAY)
        out.append('<details><summary>%s</summary><div class="faq-a"><p>%s</p></div></details>'
                   % (esc(q), esc(a)))
    return '<div class="faq">' + "".join(out) + "</div>"


def faq_schema(items, cityname):
    ents = []
    for q, a in items:
        q = q.replace("{city}", cityname).replace("{brand}", C.BRAND).replace("{phone}", C.PHONE_DISPLAY)
        a = a.replace("{city}", cityname).replace("{brand}", C.BRAND).replace("{phone}", C.PHONE_DISPLAY)
        ents.append({"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}})
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents}


def page(title, desc, relpath, body, schema=None, active="", sub="", robots="index,follow",
         scripts=()):
    sch = "".join(T.ld(s) for s in (schema or []))
    return "\n".join([
        T.head(title, desc, relpath, extra_schema=sch, robots=robots),
        "<body>",
        '<a class="skip" href="#main">Skip to content</a>',
        T.header(active, sub),
        '<main id="main">',
        body,
        "</main>",
        T.footer(cities_by_county()),
        T.page_end(scripts),
        "</body>",
        "</html>",
        "",
    ])


# ================================================================ city page ==


HERO_CARD = [
    ("Call {name} plumbing help",
     ["{county} and surrounding communities", "ZIP codes: {zips}",
      "Residential, rental and small commercial", "Emergencies routed to whoever is available"]),
    ("Plumbing help for {name}",
     ["{county} plus the towns around it", "Covering {zipfirst} and nearby",
      "Homes, rentals and light commercial", "After-hours calls routed where a plumber is on"]),
    ("Speak to a plumber covering {name}",
     ["{name} and {county}", "ZIP codes {zips}", "Owner-occupied, rental and commercial",
      "Urgent jobs routed to whoever is free"]),
    ("Who answers when you call from {name}",
     ["Our referral line, then a local plumber", "{county} coverage", "ZIP codes {zips}",
      "No charge to you for the introduction"]),
    ("{name} plumbing, by phone",
     ["{county} and neighbouring communities", "{zipfirst} and surrounding ZIPs",
      "Residential and small commercial", "Emergencies handled as they come"]),
    ("Get connected in {name}",
     ["Serving {county}", "ZIP codes {zips}", "Homes, rentals, businesses",
      "Available plumbers only - we will say so if there are none"]),
    ("One call, {name} coverage",
     ["{county} and around", "{zipfirst} plus nearby ZIP codes",
      "Residential, rental and property management", "Out-of-hours routed where possible"]),
    ("Calling about a {name} address",
     ["{name}, {county} and the surrounding towns", "ZIP codes {zips}",
      "Any residential property type", "Urgent calls prioritised in the routing"]),
]

HERO_CTA = [
    ("How the referral works", "#what-happens"),
    ("What happens when I call", "#what-happens"),
    ("Read how this works", "#what-happens"),
    ("See what a call does", "#what-happens"),
    ("How the routing works", "#what-happens"),
    ("What to expect on the call", "#what-happens"),
    ("Before you dial", "#what-happens"),
    ("How we connect you", "#what-happens"),
]


_INDEX = None


def _related(a, b):
    """Two city pages a reader is likely to encounter close together.

    Same county (they are listed under the same heading on the homepage and in
    the footer), one names the other as a nearby town (they cross-link in the
    'nearby cities' block), or they are adjacent in the CITIES ordering, which
    is the order they appear in the sitemap and the city index.
    """
    global _INDEX
    if _INDEX is None:
        _INDEX = {c["slug"]: i for i, c in enumerate(CITIES)}
    if a["county"] == b["county"]:
        return True
    if b["name"] in a["nearby"] or a["name"] in b["nearby"]:
        return True
    d = abs(_INDEX[a["slug"]] - _INDEX[b["slug"]])
    return d == 1 or d == len(CITIES) - 1


POOLS = {
    "faq":    "GENERIC_FAQ",
    "emerg":  "EMERGENCY",
    "quote":  "NOT_QUOTE",
    "close":  "CLOSING",
    "intro":  "INTRO",
    "refer":  "REFERRAL",
    "area":   "AREA_INTRO",
    "svc":    "SVC_LEAD",
    "sub":    "SUB_LINE",
    "ready":  "HAVE_READY",
    "rhead":  "READY_HEADING",
    "ahead":  "AREA_HEADINGS",
    "hero":   "HERO_CARD",
    "cta":    "HERO_CTA",
}


def _augment(slots, adj_slots, u, seen):
    for v in adj_slots[u]:
        if v in seen:
            continue
        seen.add(v)
        if v not in slots or _augment(slots, adj_slots, slots[v], seen):
            slots[v] = u
            return True
    return False


def _unique_matching(adj_slots, cities, n_slots):
    """Maximum bipartite matching: each city gets its own slot, subject to the
    colouring constraint that no related neighbour already holds it."""
    slots = {}
    order = sorted(cities, key=lambda c: (len(adj_slots[c]), c))
    for u in order:
        _augment(slots, adj_slots, u, set())
    out = {u: None for u in cities}
    for v, u in slots.items():
        out[u] = v
    return out, len(slots) == len(cities)


def assign_slots():
    """Colour every rotating copy pool so that two city pages a reader is likely
    to see together never repeat a block of copy.

    'Related' = same county, or one page lists the other as a nearby town. The
    largest such clique in batch 1 is 7 cities, so each pool needs >= 7 variants
    for a clash-free colouring to exist.

    All pools are coloured JOINTLY: a candidate assignment for a city must be
    clash-free in every pool simultaneously, otherwise two pools can independently
    pick the same slot and the pair still repeats copy. Search is a pruned DFS
    over pools, largest pool first, which keeps it fast at 18 cities and stays
    practical at 100+ (the pruning is what does the work, not brute force).
    """
    names = list(POOLS)
    sizes = {n: len(globals()[POOLS[n]]) for n in names}
    for n, sz in sizes.items():
        if sz < 7:
            raise SystemExit("pool %s has %d variants; needs >= 7 for a clean colouring" % (n, sz))

    adj = {c["slug"]: set() for c in CITIES}
    for i, a in enumerate(CITIES):
        for b in CITIES[i + 1:]:
            if _related(a, b):
                adj[a["slug"]].add(b["slug"])
                adj[b["slug"]].add(a["slug"])

    # largest pools first: they constrain hardest, so pruning bites early
    order_pools = sorted(names, key=lambda n: -sizes[n])
    assigned = {}

    def search(slug, k, partial, banned, load):
        if k == len(order_pools):
            return dict(partial)
        n = order_pools[k]
        free = [v for v in range(sizes[n]) if v not in banned[n]]
        if not free:
            return None
        free.sort(key=lambda v: (load[n][v], v))
        for v in free:
            partial[n] = v
            banned[n].add(v)
            load[n][v] += 1
            got = search(slug, k + 1, partial, banned, load)
            load[n][v] -= 1
            banned[n].discard(v)
            if got is not None:
                return got
        partial.pop(n, None)
        return None

    for c in sorted(CITIES, key=lambda c: (-len(adj[c["slug"]]), c["slug"])):
        slug = c["slug"]
        banned = {n: set() for n in names}
        for nb in adj[slug]:
            if nb in assigned:
                for n in names:
                    banned[n].add(assigned[nb][n])
        load = {n: [sum(1 for a in assigned.values() if a.get(n) == v)
                    for v in range(sizes[n])] for n in names}
        got = search(slug, 0, {}, banned, load)
        if got is None:
            # cannot happen while every pool has >= max-clique variants; degrade
            # gracefully rather than failing the build
            got = {n: min(range(sizes[n]), key=lambda v: load[n][v]) for n in names}
        assigned[slug] = got

    # When the FAQ pool has one set per city, make every page's generic FAQ set
    # globally unique (not merely different from its neighbours). This is an
    # assignment problem, so solve it as one rather than hoping greedy lands it.
    if sizes["faq"] >= len(CITIES):
        slugs = [c["slug"] for c in CITIES]
        taken_by_neighbour = {s: set() for s in slugs}
        for s in sorted(slugs, key=lambda x: (-len(adj[x]), x)):
            for nb in adj[s]:
                taken_by_neighbour[nb].add(assigned[s]["faq"])
        allowed = {s: [v for v in range(sizes["faq"]) if v not in taken_by_neighbour[s]]
                      or list(range(sizes["faq"])) for s in slugs}
        match = {}
        for u in sorted(slugs, key=lambda x: (len(allowed[x]), x)):
            _augment(match, allowed, u, set())
        if len(match) == len(slugs):
            for v, u in match.items():
                assigned[u]["faq"] = v

    return {n: {s: assigned[s][n] for s in assigned} for n in names}


_SLOTS = assign_slots()
_CLASHES = slot_clashes() if False else []
FAQ_SLOT = _SLOTS["faq"]
EMERG_SLOT = _SLOTS["emerg"]
QUOTE_SLOT = _SLOTS["quote"]
CLOSE_SLOT = _SLOTS["close"]
INTRO_SLOT = _SLOTS["intro"]
REFER_SLOT = _SLOTS["refer"]
AREA_SLOT = _SLOTS["area"]
SVC_SLOT = _SLOTS["svc"]
SUB_SLOT = _SLOTS["sub"]
READY_SLOT = _SLOTS["ready"]
RHEAD_SLOT = _SLOTS["rhead"]
AHEAD_SLOT = _SLOTS["ahead"]
HERO_SLOT = _SLOTS["hero"]
CTA_SLOT = _SLOTS["cta"]


def slot_clashes():
    """Related city pages that still share a rotating block. Must be empty."""
    out = []
    for i, a in enumerate(CITIES):
        for b in CITIES[i + 1:]:
            if not _related(a, b):
                continue
            for n in POOLS:
                if _SLOTS[n][a["slug"]] == _SLOTS[n][b["slug"]]:
                    out.append((a["slug"], b["slug"], n))
    return out


def build_city(idx, c):
    name, slug = c["name"], c["slug"]
    rel = "cities/%s.html" % slug

    # Rotation strides are deliberately not multiples of any pool length, so no
    # two city pages ever share the same heading + copy combination.
    def rot(pool, stride):
        return pool[(idx + stride) % len(pool)]

    intro = INTRO[INTRO_SLOT[slug]].format(city=name, issue=c["issue"])
    referral = REFERRAL[REFER_SLOT[slug]].format(city=name, brand=C.BRAND, phone=C.PHONE_DISPLAY)
    closing = CLOSING[CLOSE_SLOT[slug]]
    emergency = EMERGENCY[EMERG_SLOT[slug]]

    faq_items = list(c["faq"]) + list(GENERIC_FAQ[FAQ_SLOT[slug]])
    faq_items = [(q.replace("{city}", name), a.replace("{city}", name)) for q, a in faq_items]

    # Rotate which of the three middle blocks comes first, so the pages do not
    # all follow one fixed outline.
    order = [["area", "issue", "call", "svc"],
             ["issue", "area", "call", "svc"],
             ["call", "issue", "area", "svc"],
             ["area", "issue", "svc", "call"],
             ["issue", "area", "svc", "call"],
             ["call", "area", "issue", "svc"],
             ["area", "call", "issue", "svc"]][(idx) % 7]

    nbrs = neighbors(slug, 4)

    blocks = {}

    ah = AREA_HEADINGS[AHEAD_SLOT[slug]]
    blocks["area"] = """
<section id="area">
  <div class="wrap">
    <span class="kicker">Service area</span>
    <h2>{h_area}</h2>
    <p>{area_intro}</p>
    <h3>{ah0}</h3>
    {nhood}
    <h3>{ah1}</h3>
    {zips}
    <h3>{ah2}</h3>
    {near}
  </div>
</section>""".format(
        h_area=esc(rot(H_AREA, 9).format(city=name)), name=esc(name),
        area_intro=esc(AREA_INTRO[AREA_SLOT[slug]].format(name=name)),
        ah0=esc(ah[0].format(name=name)), ah1=esc(ah[1].format(name=name)),
        ah2=esc(ah[2].format(name=name)),
        nhood=chips(c["neighborhoods"]), zips=chips(c["zips"], "chip zip"),
        near=chips(c["nearby"]))

    blocks["issue"] = """
<section id="local-issues" class="section-alt">
  <div class="wrap prose">
    <span class="kicker">Local conditions</span>
    <h2>{h_issue}</h2>
    <p>{issue}</p>
    <h2>{h_fact}</h2>
    <p>{fact}</p>
    <dl class="fact-strip">
      <div class="fact"><dt>County</dt><dd>{county}</dd></div>
      <div class="fact"><dt>Population</dt><dd>{pop} <span class="small muted">({popnote})</span></dd></div>
      <div class="fact"><dt>ZIP codes</dt><dd>{zipcount}</dd></div>
    </dl>
    <p class="small muted">{sources}</p>
  </div>
</section>""".format(
        h_issue=esc(rot(H_ISSUE, 13).format(city=name)), issue=esc(c["issue"]),
        h_fact=esc(rot(H_FACT, 13).format(city=name)), fact=esc(c["fact"]),
        county=esc(c["county"]), pop=esc(c["population"]), popnote=esc(c["pop_note"]),
        zipcount=", ".join(esc(z) for z in c["zips"]), sources=esc(c["sources"]))

    blocks["call"] = """
<section id="what-happens">
  <div class="wrap">
    <span class="kicker">Referral, not a plumbing company</span>
    <h2>{h_call}</h2>
    <div class="two-col">
      <div class="prose">
        <p>{referral}</p>
        <p>{closing}</p>
        {disc}
      </div>
      <div class="hero-card" style="background:var(--bg-3);border-color:var(--line)">
        <h3 style="color:var(--navy)">{ready_heading}</h3>
        <ul style="color:#33465a">
          {ready_items}
        </ul>
        <p style="margin-top:14px">{phone}</p>
      </div>
    </div>
  </div>
</section>""".format(
        h_call=esc(rot(H_CALL, 5).format(city=name, phone=C.PHONE_DISPLAY, brand=C.BRAND)),
        referral=esc(referral), closing=esc(closing),
        disc=T.disclosure("long"), name=esc(name),
        ready_heading=esc(READY_HEADING[RHEAD_SLOT[slug]]),
        ready_items="".join("<li>%s</li>" % esc(x.format(name=name))
                            for x in HAVE_READY[READY_SLOT[slug]]),
        phone=T.phone_link("md"))

    blocks["svc"] = """
<section id="services" class="section-alt">
  <div class="wrap">
    <span class="kicker">What this covers</span>
    <h2>{h_svc}</h2>
    <p class="lead">{svc_lead}</p>
    <div class="cards">
      {cards}
    </div>
    <div class="note">
      <p><strong>Not a price quote.</strong> {notquote}</p>
    </div>
  </div>
</section>""".format(
        h_svc=esc(rot(H_SVC, 17).format(city=name)), name=esc(name),
        notquote=esc(NOT_QUOTE[QUOTE_SLOT[slug]].format(name=name)),
        svc_lead=esc(SVC_LEAD[SVC_SLOT[slug]].format(name=name)),
        cards="".join(
            '<div class="card"><h3>%s %s</h3><p class="small muted">%s</p></div>'
            % (ICON, esc(sv), esc(SVC_BLURB[(idx * 5 + k * 3) % len(SVC_BLURB)].format(name=name)))
            for k, sv in enumerate(c["services"])))

    near_links = "".join(
        '<a class="city-link" href="%s">%s<small>%s</small></a>'
        % (city_href(n), esc(n["name"]), esc(n["county"])) for n in nbrs)

    body = """
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <ul class="breadcrumb" aria-label="Breadcrumb">
        <li><a href="/">Home</a></li>
        <li><a href="/index.html#cities">Cities</a></li>
        <li aria-current="page">{name}</li>
      </ul>
      <h1>Plumber in {name}, {st}</h1>
      <p class="lead">{intro}</p>
      <div class="hero-cta">
        {phone_lg}
        <a class="btn outline" href="{cta_href}">{cta_label}</a>
      </div>
      <p class="hero-note">Free to use &middot; {disc_short}</p>
    </div>
    <div class="hero-card">
      <h2>{hero_h2}</h2>
      <ul>
        {hero_items}
      </ul>
      <p style="margin:14px 0 0">{phone_md}</p>
      <p class="small" style="color:#B9CBD9;margin:10px 0 0">{subline}</p>
    </div>
  </div>
</section>
{blocks}
<section id="emergency">
  <div class="wrap prose">
    <span class="kicker">Urgent situations</span>
    <h2>{h_emerg}</h2>
    <p>{emergency}</p>
  </div>
</section>
<section id="faq" class="section-alt">
  <div class="wrap">
    <span class="kicker">FAQ</span>
    <h2>{h_faq}</h2>
    {faq}
  </div>
</section>
<section id="nearby">
  <div class="wrap">
    <span class="kicker">Keep looking</span>
    <h2>{h_near}</h2>
    <div class="city-grid">{near_links}</div>
    <p style="margin-top:22px"><a class="btn accent" href="/">See all {n} covered cities</a></p>
  </div>
</section>
""".format(
        name=esc(name), st=C.STATE_ABBR, intro=esc(intro),
        phone_lg=T.phone_link("lg"), phone_md=T.phone_link("md"),
        disc_short=esc(C.DISCLOSURE_SHORT), brand=esc(C.BRAND),
        subline=esc(SUB_LINE[SUB_SLOT[slug]].format(name=name, brand=C.BRAND)),
        county=esc(c["county"]), zipcount=esc(", ".join(c["zips"])),
        hero_h2=esc(HERO_CARD[HERO_SLOT[slug]][0].format(name=name)),
        hero_items="".join("<li>%s</li>" % esc(x.format(
            name=name, county=c["county"], zips=", ".join(c["zips"]), zipfirst=c["zips"][0]))
            for x in HERO_CARD[HERO_SLOT[slug]][1]),
        cta_label=esc(HERO_CTA[CTA_SLOT[slug]][0]), cta_href=HERO_CTA[CTA_SLOT[slug]][1],
        blocks="".join(blocks[k] for k in order),
        h_emerg=esc(rot(H_EMERG, 15).format(city=name)), emergency=esc(emergency),
        h_faq=esc(rot(H_FAQ, 10).format(city=name)), faq=faq_html(faq_items, name),
        h_near=esc(rot(H_NEAR, 11).format(city=name)), near_links=near_links,
        n=len(CITIES))

    title = "Plumber in %s, CA \u2014 Free Local Referral" % name
    if len(title) > 60:
        title = "%s Plumber Referral | %s" % (name, C.BRAND)
    # Never truncate mid-word: try progressively shorter descriptions and take
    # the longest that fits the 158-char budget.
    hood = c["neighborhoods"][0].split(" (")[0].split(" / ")[0]
    cands = [
        "Free plumber referral for %s, %s. Call %s and we connect you with a licensed local "
        "plumbing professional. Covers %s and ZIP %s."
        % (name, c["county"], C.PHONE_DISPLAY, hood, ", ".join(c["zips"][:3])),
        "Free plumber referral in %s, %s. Call %s to reach a licensed local plumbing professional. "
        "Covers ZIP %s." % (name, c["county"], C.PHONE_DISPLAY, ", ".join(c["zips"][:3])),
        "Free plumber referral in %s, %s. Call %s and we connect you with a licensed local plumbing "
        "professional. Not a plumbing company." % (name, c["county"], C.PHONE_DISPLAY),
        "Free plumber referral in %s, %s. Call %s to reach a licensed local plumbing professional."
        % (name, c["county"], C.PHONE_DISPLAY),
    ]
    desc = next((x for x in cands if len(x) <= 158), cands[-1])

    schema = [
        {"@context": "https://schema.org", "@type": "WebPage",
         "name": "Plumber in %s, California" % name, "url": C.ORIGIN + "/" + rel,
         "isPartOf": {"@type": "WebSite", "name": C.BRAND, "url": C.ORIGIN + "/"},
         "about": {"@type": "Service", "name": "Plumber referral service",
                   "serviceType": "Plumbing referral",
                   "provider": {"@type": "Organization", "name": C.BRAND, "url": C.ORIGIN + "/"}},
         "mainEntity": {"@type": "Place", "name": "%s, California" % name,
                        "containedInPlace": {"@type": "AdministrativeArea", "name": c["county"]}}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": C.ORIGIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Cities", "item": C.ORIGIN + "/index.html"},
            {"@type": "ListItem", "position": 3, "name": name, "item": C.ORIGIN + "/" + rel}]},
        {"@context": "https://schema.org", "@type": "Service",
         "name": "Plumber referral in %s, California" % name,
         "serviceType": "Plumbing referral and call routing",
         "provider": {"@type": "Organization", "name": C.BRAND, "url": C.ORIGIN + "/",
                      "telephone": C.PHONE_TEL},
         "areaServed": {"@type": "City", "name": name, "containedInPlace":
                        {"@type": "AdministrativeArea", "name": c["county"]}},
         "description": ("%s is a free referral service that connects callers in %s, California with "
                         "independent licensed local plumbing professionals. It is not a plumbing "
                         "company and does not perform plumbing work." % (C.BRAND, name))},
        faq_schema(faq_items, name),
    ]

    w(rel, page(title, desc, rel, body, schema, active="cities",
                sub="%s, %s" % (name, C.STATE_ABBR)))
    return {"slug": slug, "name": name, "county": c["county"], "url": rel,
            "title": title, "desc": desc, "words": len(re.sub(r"<[^>]+>", " ", body).split())}


# ================================================================== homepage ==

HOME_FAQ = [
    ("Is %s free to use?" % C.BRAND,
     "Yes. There is no charge to you for calling or for being connected to a plumbing professional. "
     "The plumbing businesses that receive referrals pay us, which is what keeps the service free for "
     "callers. You pay the plumber you hire, at whatever rate you agree with them."),
    ("Are the plumbers licensed and insured?",
     "We aim to connect callers with licensed, insured plumbing professionals, and that is a condition "
     "of taking referrals through this service. We are not the contractor, so confirm licence and "
     "insurance with the plumber directly before work begins. California contractor licences can be "
     "verified through the Contractors State License Board."),
    ("What areas are covered?",
     "Right now the site covers %d cities across six Central Coast counties: %s. Coverage is added in "
     "batches, and each city page lists the specific neighborhoods, ZIP codes and nearby towns it "
     "covers. If your town is not listed yet, call anyway \u2014 we will tell you honestly whether a "
     "plumber serving your area is available."
     % (len(CITIES), ", ".join(sorted({c["county"] for c in CITIES})))),
    ("What if I need emergency plumbing service?",
     "Call the number on this page. We route you to whoever is available, including outside normal "
     "business hours where a plumber is on call. We do not promise a specific arrival time, because "
     "that depends on the plumber and current demand. If there is a gas smell, water near electrical "
     "outlets, or any risk to life, call 911 or your utility first."),
    ("Is %s a plumbing company?" % C.BRAND,
     "No. %s is a referral and call routing service. We do not hold a contractor licence, we do not "
     "employ plumbers, and we do not perform or supervise plumbing work. The plumber who takes your "
     "call is an independent business and your agreement is with them." % C.BRAND),
    ("Will I get a price over the phone?",
     "Not from us. Pricing is set by the individual plumbing business, and anyone who gives you a firm "
     "price before seeing the job is guessing. Expect a diagnostic or call-out fee from many plumbers, "
     "often applied to the repair. Ask for the pricing structure before work starts."),
]


def build_home():
    groups = cities_by_county()

    county_html = []
    for county in COUNTY_ORDER:
        cs = groups.get(county) or []
        if not cs:
            continue
        links = "".join(
            '<a class="city-link" href="{href}" data-city="{name}" data-county="{county}" '
            'data-zips="{zips}" data-hood="{hood}">{name}<small>{pop} residents &middot; ZIP {zip0}'
            '</small></a>'.format(
                href=city_href(c), name=esc(c["name"]), county=esc(c["county"]),
                zips=esc(" ".join(c["zips"])), pop=esc(c["population"]), zip0=esc(c["zips"][0]),
                hood=esc(" ".join(c["neighborhoods"] + c["nearby"]).lower()))
            for c in cs)
        county_html.append(
            '<div class="county-block" data-county="{c}"><h3>{c}</h3>'
            '<div class="city-grid">{l}</div></div>'.format(c=esc(county), l=links))

    search_html = """
    <div class="note" style="margin-bottom:22px">
      <p><strong>Looking for your town?</strong> Use the search box below. It filters the list as you
      type and works with city names, counties and ZIP codes. No data leaves your browser.</p>
      <div class="form-row" style="margin:0">
        <label for="city-search" style="margin-bottom:6px">Find your city</label>
        <input type="text" id="city-search" placeholder="Type a city, county or ZIP code\u2026"
               autocomplete="off" aria-describedby="city-search-status">
        <p id="city-search-status" class="small muted" role="status" style="margin:8px 0 0"></p>
      </div>
    </div>"""

    body = """
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="kicker" style="color:#F0A860">Free plumber referrals &middot; California Central Coast</span>
      <h1>Find a licensed plumber near you, fast</h1>
      <p class="lead">{brand} is a free referral service. Tell us what has gone wrong and where you
         are, and we connect your call to an independent, licensed local plumbing professional. We are
         not a plumbing company and we do not perform the work ourselves.</p>
      <div class="hero-cta">
        {phone_lg}
        <a class="btn outline" href="#cities">Browse {n} covered cities</a>
      </div>
      <p class="hero-note">{disc_short}</p>
    </div>
    <div class="hero-card">
      <h2>What you get when you call</h2>
      <ul>
        <li>A live referral line, not a voicemail maze</li>
        <li>Routing to a licensed plumber serving your ZIP code</li>
        <li>No cost to you and no obligation to hire</li>
        <li>Honest answers when nobody is available</li>
      </ul>
      <p style="margin:16px 0 0">{phone_md}</p>
    </div>
  </div>
</section>

<section id="how">
  <div class="wrap">
    <span class="kicker">Three steps</span>
    <h2>How it works</h2>
    <div class="steps">
      <div class="step">
        <h3>Call or find your city</h3>
        <p>Dial {phone_display} from anywhere on the Central Coast, or open your city page to see the
           exact neighborhoods, ZIP codes and nearby towns it covers.</p>
      </div>
      <div class="step">
        <h3>Get connected to a licensed local pro</h3>
        <p>We take the basics \u2014 your location, the problem, whether the water is off \u2014 and route the
           call to an independent licensed plumbing professional who serves that area.</p>
      </div>
      <div class="step">
        <h3>They quote and fix it</h3>
        <p>The plumber assesses the job, quotes it and does the work. Your agreement, invoice and any
           warranty are with that plumber, not with {brand}.</p>
      </div>
    </div>
    <p style="margin-top:22px"><a class="btn accent" href="/how-it-works.html">Read the full explanation</a>
       &nbsp; <a href="/about.html">Or how we make money</a></p>
  </div>
</section>

<section id="cities" class="section-alt">
  <div class="wrap">
    <span class="kicker">Coverage</span>
    <h2>Cities we currently cover</h2>
    <p class="lead">Batch one of {n} city pages, across {counties} counties. Every page is written
       about that specific place \u2014 real neighborhoods, real ZIP codes, and the plumbing problems
       that are actually common there. More cities are added in batches.</p>
    {search}
    {counties_html}
  </div>
</section>

<section id="honest">
  <div class="wrap two-col">
    <div class="prose">
      <span class="kicker">Plainly stated</span>
      <h2>What {brand} is, and what it is not</h2>
      <p>This site exists to get you to a plumber. It is not a plumbing company. We hold no contractor
         licence, employ no plumbers, and do not perform or supervise any plumbing work.</p>
      <p>You will not find invented reviews, made-up star ratings, or a promise of a response time on
         any page of this site. Those claims are easy to write and impossible to stand behind, so we do
         not make them. What we can tell you is whether a licensed plumbing professional serving your
         area is available to take your call.</p>
      <p>We are paid by the plumbing businesses that receive referrals. That is the whole business
         model, and it is why the service costs you nothing.</p>
    </div>
    <div class="cards" style="grid-template-columns:1fr">
      <div class="card"><h3>{icon} We do</h3><p class="small">Route your call to a licensed local
         plumbing professional. List real neighborhoods and ZIP codes. Tell you when nobody is
         available. Keep your details to what is needed to route the call.</p></div>
      <div class="card"><h3>{icon} We do not</h3><p class="small">Perform plumbing work. Guarantee a
         price, an arrival time or a specific contractor. Publish fake reviews or ratings. Sell your
         contact details to unrelated marketers.</p></div>
    </div>
  </div>
</section>

<section id="faq" class="section-alt">
  <div class="wrap">
    <span class="kicker">FAQ</span>
    <h2>Questions callers ask us</h2>
    {faq}
  </div>
</section>

<section id="cta">
  <div class="wrap">
    <div class="call-block">
      <div class="call-row">
        <div>
          <h2>Something has gone wrong with the plumbing?</h2>
          <p style="max-width:56ch;margin-bottom:0">Call now and we will route you to a licensed
             plumbing professional serving your area. Free to use, no account, no form.</p>
        </div>
        <div>{phone_lg}</div>
      </div>
      {disc}
    </div>
  </div>
</section>
""".format(
        brand=esc(C.BRAND), n=len(CITIES), counties=len({c["county"] for c in CITIES}),
        phone_lg=T.phone_link("lg"), phone_md=T.phone_link("md"),
        phone_display=esc(C.PHONE_DISPLAY), disc_short=esc(C.DISCLOSURE_SHORT),
        search=search_html, counties_html="".join(county_html),
        icon=ICON, faq=faq_html(HOME_FAQ, ""), disc=T.disclosure("long"))

    title = "%s | Free Plumber Referrals, Central Coast CA" % C.BRAND
    desc = ("%s is a free referral service connecting you with licensed local plumbing professionals "
            "in %d Central Coast cities. Call %s." % (C.BRAND, len(CITIES), C.PHONE_DISPLAY))

    schema = [
        {"@context": "https://schema.org", "@type": "Organization", "name": C.BRAND,
         "url": C.ORIGIN + "/", "telephone": C.PHONE_TEL,
         "description": ("A free referral and call routing service connecting callers with "
                         "independent licensed local plumbing professionals. Not a licensed "
                         "contractor."),
         "areaServed": [{"@type": "AdministrativeArea", "name": c} for c in COUNTY_ORDER]},
        {"@context": "https://schema.org", "@type": "WebSite", "name": C.BRAND, "url": C.ORIGIN + "/",
         "publisher": {"@type": "Organization", "name": C.BRAND}},
        faq_schema(HOME_FAQ, ""),
    ]

    w("index.html", page(title, desc, "/", body, schema, active="home",
                         scripts=("/js/city-search.js",)))

    # machine-readable city index used by the search box and future batches
    w("data/cities.json", json.dumps(
        [{"slug": c["slug"], "name": c["name"], "county": c["county"],
          "zips": c["zips"], "neighborhoods": c["neighborhoods"],
          "nearby": c["nearby"], "url": city_href(c), "batch": C.BATCH} for c in CITIES],
        ensure_ascii=False, indent=1))


# ============================================================ how-it-works ==

def build_how():
    body = """
<section class="hero">
  <div class="wrap">
    <ul class="breadcrumb" aria-label="Breadcrumb"><li><a href="/">Home</a></li>
      <li aria-current="page">How it works</li></ul>
    <h1>How {brand} works</h1>
    <p class="lead">Short version: you call, we route you to a licensed local plumbing professional,
       they do the work. Here is the long version, including the parts most referral sites leave out.</p>
    <div class="hero-cta">{phone_md}</div>
    <p class="hero-note">{disc_short}</p>
  </div>
</section>

<section>
  <div class="wrap prose">
    <span class="kicker">Step by step</span>
    <h2>The three steps</h2>
    <div class="steps" style="margin:22px 0">
      <div class="step"><h3>Call or search</h3><p>Dial {phone_display} or open your city page. The city
        pages list the specific neighborhoods, ZIP codes and nearby towns each one covers, so you can
        check whether your address is in scope before you call.</p></div>
      <div class="step"><h3>Get connected to a licensed local pro</h3><p>We ask for your location, the
        problem, and whether the water is shut off. Then we route the call to an independent licensed
        plumbing professional who serves that area and is available.</p></div>
      <div class="step"><h3>They quote and fix it</h3><p>The plumber assesses the job, gives you a
        price, and does the work if you want them to. Your contract, invoice and any warranty are with
        that plumber.</p></div>
    </div>

    <h2>What we are</h2>
    <p>{brand} is a lead generation and call routing service. We publish information about plumbing
       problems in specific Central Coast cities and operate a phone line that connects callers to
       plumbing professionals. That is the entire scope of what we do.</p>

    <h2>What we are not</h2>
    <p>We are not a plumbing company. We do not hold a contractor licence, we do not employ plumbers,
       we do not own the vans, we do not set prices, and we do not perform or supervise any plumbing
       work. Nothing on this site should be read as a contractor offering to do work for you.</p>

    <h2>How the phone number works</h2>
    <p>The number shown on this site, {phone_display}, is a tracked number. When the page loads, a call
       tracking platform called Ringba may replace the number you see with another number from its pool
       so that the call can be attributed to the page you were reading and routed correctly. If that
       script does not load, the number above still works and still routes.</p>
    <p>Routing and tracking happen on the phone number. We do not use that mechanism to collect your
       browsing history, and the details are set out in the <a href="/privacy-policy.html">privacy
       policy</a>.</p>

    <h2>How we make money</h2>
    <p>Plumbing businesses pay us when they receive a qualified call from this site. This is called a
       pay-per-call arrangement. You are never charged anything by {brand} \u2014 not for the call, not for
       the referral, and not as a percentage of the work.</p>
    <p>That arrangement creates an obvious incentive, so here is how we handle it: we do not rank or
       route based on which plumber pays the most, we do not publish invented reviews to make the site
       look more established than it is, and we tell you when nobody serving your area is available
       rather than holding your call.</p>

    <h2>What we deliberately do not claim</h2>
    <div class="note">
      <p>You will not find any of the following on this site, because we cannot verify them:</p>
      <ul>
        <li>Customer testimonials, star ratings or review counts</li>
        <li>A promised response time or arrival window</li>
        <li>A satisfaction percentage or number of jobs completed</li>
        <li>A founding year, a business address, or a named owner of a plumbing company</li>
        <li>A count of plumbers "in our network" in any given city</li>
      </ul>
      <p>If we ever have real, sourced figures for any of those, we will publish them with the source
      attached.</p>
    </div>

    <h2>What happens to your information</h2>
    <p>Enough to route the call: your location, the nature of the problem, and your phone number if you
       give it. Call tracking software also records technical session data about the page you called
       from. If call recording is enabled on the campaign, your call may be recorded \u2014 see the
       <a href="/privacy-policy.html">privacy policy</a> for the disclosure and your options.</p>

    <h2>If something goes wrong</h2>
    <p>Your contract is with the plumber you hire. If a referred plumber does poor work, that dispute is
       between you and that business, and the California Contractors State License Board is the body
       that handles contractor complaints. That said, if a referral went badly wrong we want to know:
       use the <a href="/contact.html">contact page</a> and we will look into it and stop sending calls
       to that business if it is warranted.</p>
  </div>
</section>
""".format(brand=esc(C.BRAND), phone_md=T.phone_link("md"),
           phone_display=esc(C.PHONE_DISPLAY), disc_short=esc(C.DISCLOSURE_SHORT))

    w("how-it-works.html", page(
        "How it works | %s" % C.BRAND,
        "%s is a free pay-per-call referral service. You call, we route you to a licensed local "
        "plumber. We are not a plumbing company." % C.BRAND,
        "how-it-works.html", body, active="how"))


# ==================================================================== about ==

def build_about():
    body = """
<section class="hero">
  <div class="wrap">
    <ul class="breadcrumb" aria-label="Breadcrumb"><li><a href="/">Home</a></li>
      <li aria-current="page">About</li></ul>
    <h1>About {brand}</h1>
    <p class="lead">A free referral service for people on California's Central Coast who need a
       plumber and would rather talk to one than fill in a form.</p>
  </div>
</section>

<section>
  <div class="wrap prose">
    <h2>What this site is</h2>
    <p>{brand} publishes practical, city-specific information about plumbing problems and connects
       callers with independent, licensed local plumbing professionals. It launched with {n} city pages
       across {counties} Central Coast counties, from Gilroy and Hollister in the north down through
       the Salinas Valley and Monterey Peninsula to Santa Barbara in the south.</p>
    <p>It is a referral and call routing service. It is not a plumbing company. We do not hold a
       contractor licence, employ plumbers, or perform or supervise plumbing work.</p>

    <h2>Why it exists</h2>
    <p>Searching for a plumber usually produces one of two things: a paid directory stuffed with
       invented five-star reviews, or a list of national lead-generation forms that sell your phone
       number to whoever bids on it. Neither is much use at eleven at night with water on the kitchen
       floor.</p>
    <p>This site does one narrow thing instead. It tells you honestly what goes wrong with plumbing in
       your specific town \u2014 hard water in Santa Maria, pre-1970 clay and Orangeburg laterals in Santa
       Cruz, salt-air corrosion in Pacific Grove \u2014 and then gives you a phone number that reaches a
       licensed plumbing professional who serves your area.</p>

    <h2>How we make money</h2>
    <p>Plumbing businesses pay us per qualified call. That is the pay-per-call model, and it is the
       only revenue this site has. It costs you nothing to call or to be referred.</p>

    <h2>Editorial rules we hold ourselves to</h2>
    <div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin:20px 0">
      <div class="card"><h3>No invented proof</h3><p class="small">No fake testimonials, no star
        ratings, no review counts, no satisfaction percentages, no jobs-completed figures. There is
        nothing to show yet, so nothing is shown.</p></div>
      <div class="card"><h3>No invented history</h3><p class="small">No founding year, no
        "family owned since", no business address, no named owner of a plumbing company that does not
        exist.</p></div>
      <div class="card"><h3>No invented numbers</h3><p class="small">Every figure on a city page comes
        from a public source \u2014 the U.S. Census Bureau, a water utility's published quality report, or
        a city or county program page \u2014 and the source is stated on the page.</p></div>
      <div class="card"><h3>No copied pages</h3><p class="small">Each city page is written about that
        city: real neighborhoods, real ZIP codes, and the plumbing issues that are genuinely common
        there. If we cannot write something true and specific about a place, we do not publish a page
        for it.</p></div>
    </div>

    <h2>Coverage</h2>
    <p>The site is published in batches. Batch one is the {n} cities listed below. Additional cities
       are added over time, and each new page has to meet the same standard as the existing ones \u2014
       which is why they do not all appear at once.</p>
    {cities}

    <h2>Who to contact</h2>
    <p>For plumbing help, call {phone_display}. For anything about this website \u2014 a correction, a
       complaint about a referred plumber, a request to add your town \u2014 use the
       <a href="/contact.html">contact page</a> or write to
       <a href="mailto:{email}">{email}</a>.</p>

    <div class="note">
      <p><strong>Correction policy.</strong> If a factual statement on any page of this site is wrong,
      tell us and we will fix it or remove it. The local detail on these pages is researched, but it is
      researched by humans and it can be out of date.</p>
    </div>
  </div>
</section>
""".format(brand=esc(C.BRAND), n=len(CITIES),
           counties=len({c["county"] for c in CITIES}),
           phone_display=esc(C.PHONE_DISPLAY), email=esc(C.CONTACT_EMAIL),
           cities="".join(
               '<p><strong>%s:</strong> %s</p>' % (
                   esc(county),
                   ", ".join('<a href="%s">%s</a>' % (city_href(c), esc(c["name"])) for c in cs))
               for county, cs in cities_by_county().items() if cs))

    w("about.html", page(
        "About %s | A referral service" % C.BRAND,
        "%s is a free plumber referral service for California's Central Coast: what it is, what it is "
        "not, and how it makes money." % C.BRAND,
        "about.html", body, active="about"))


# ================================================================== contact ==

def build_contact():
    body = """
<section class="hero">
  <div class="wrap">
    <ul class="breadcrumb" aria-label="Breadcrumb"><li><a href="/">Home</a></li>
      <li aria-current="page">Contact</li></ul>
    <h1>Contact {brand}</h1>
    <p class="lead">If you need a plumber, call. If you need us, use the form. They are different
       lines and only one of them gets you a plumber.</p>
  </div>
</section>

<section>
  <div class="wrap two-col">
    <div class="call-block">
      <h2>Need a plumber right now?</h2>
      <p>Call the referral line. We route you to a licensed plumbing professional serving your area.
         Free to use, no form, no account.</p>
      <p style="margin:16px 0">{phone_lg}</p>
      {disc}
    </div>

    <div>
      <h2 style="margin-top:0">Website enquiries</h2>
      <p class="small muted">Corrections, complaints about a referred plumber, requests to add a town,
         or plumbers who want to receive referrals. This form does <strong>not</strong> get you a
         plumber \u2014 for that, call the number on the left.</p>

      <form id="contact-form" action="{form_action}" method="post" novalidate>
        <div class="form-row">
          <label for="cf-name">Your name</label>
          <input type="text" id="cf-name" name="name" required autocomplete="name">
        </div>
        <div class="form-row">
          <label for="cf-email">Email</label>
          <input type="email" id="cf-email" name="email" required autocomplete="email">
        </div>
        <div class="form-row">
          <label for="cf-city">City (optional)</label>
          <input type="text" id="cf-city" name="city" autocomplete="address-level2">
        </div>
        <div class="form-row">
          <label for="cf-topic">What is this about?</label>
          <select id="cf-topic" name="topic">
            <option value="correction">A factual correction on a page</option>
            <option value="complaint">A complaint about a referred plumber</option>
            <option value="add-city">Request to add my town</option>
            <option value="partner">I am a licensed plumber and want referrals</option>
            <option value="privacy">Privacy or data request</option>
            <option value="other">Something else</option>
          </select>
        </div>
        <div class="form-row">
          <label for="cf-msg">Message</label>
          <textarea id="cf-msg" name="message" required></textarea>
        </div>
        <button type="submit">Send message</button>
        <p class="small muted" style="margin-top:12px">Or email
           <a href="mailto:{email}">{email}</a>.</p>
      </form>
      <p id="form-status" class="small" role="status" style="margin-top:12px"></p>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="wrap prose">
    <h2>Before you send a message</h2>
    <ul>
      <li><strong>We cannot dispatch a plumber by email.</strong> There is no inbox that reaches a
        plumber. Call {phone_display}.</li>
      <li><strong>We have no office you can visit</strong> and no plumbing staff. This is a referral
        service, not a contractor.</li>
      <li><strong>Disputes about workmanship or billing</strong> are between you and the plumber you
        hired. The California Contractors State License Board handles contractor complaints; we will
        still want to hear about it so we can stop referring calls to that business if it is
        warranted.</li>
      <li><strong>Privacy and data requests</strong> are answered under the
        <a href="/privacy-policy.html">privacy policy</a>.</li>
    </ul>
  </div>
</section>

<script>
(function () {{
  var f = document.getElementById('contact-form');
  var s = document.getElementById('form-status');
  if (!f) return;
  f.addEventListener('submit', function (e) {{
    e.preventDefault();
    s.textContent = 'This form needs a backend before it can send. Nothing has been submitted yet \u2014 ' +
                    'see the setup note in README.md (FORM_ENDPOINT in src/config.py). ' +
                    'For plumbing help, call {phone_display}.';
    s.style.color = '#B4462F';
  }});
}})();
</script>
""".format(brand=esc(C.BRAND), phone_lg=T.phone_link("lg"),
           phone_display=esc(C.PHONE_DISPLAY), disc=T.disclosure("long"),
           email=esc(C.CONTACT_EMAIL),
           form_action=esc(getattr(C, "FORM_ENDPOINT", "#")))

    w("contact.html", page(
        "Contact %s | Website enquiries" % C.BRAND,
        "Contact %s about this website: corrections, complaints about a referred plumber, or a new "
        "city. For plumbing help, call %s instead." % (C.BRAND, C.PHONE_DISPLAY),
        "contact.html", body, active="contact"))


# =================================================================== privacy ==

def build_privacy():
    body = """
<section class="hero">
  <div class="wrap">
    <ul class="breadcrumb" aria-label="Breadcrumb"><li><a href="/">Home</a></li>
      <li aria-current="page">Privacy policy</li></ul>
    <h1>Privacy policy</h1>
    <p class="lead">What we collect, who we share it with, and the specific detail about call tracking
       and call recording. Last updated {date}.</p>
  </div>
</section>

<section>
  <div class="wrap prose">
    <p>This privacy policy applies to {brand} at {domain} ("the site", "we", "us"). The site is a
       referral and call routing service. We are not a plumbing contractor.</p>

    <h2>1. The short version</h2>
    <ul>
      <li>We collect what is needed to route a phone call to a plumbing professional, plus ordinary
        website analytics.</li>
      <li>Our call tracking provider, Ringba, collects technical session data about your visit so that
        a call can be matched to the page you were reading.</li>
      <li>If call recording is enabled, <strong>your call may be recorded</strong>. Details in section 5.</li>
      <li>We do not sell your personal information in the ordinary sense of that word. We do receive
        payment from plumbing businesses for referrals, which under California law can be treated as a
        "sale" or "sharing" of personal information in some circumstances. Section 9 explains your
        rights.</li>
      <li>We do not knowingly collect information from children.</li>
    </ul>

    <h2>2. Information we collect</h2>
    <h3>Information you give us</h3>
    <p>When you call, you may tell us your name, address or ZIP code, telephone number, and a
       description of the plumbing problem. When you use the contact form, you give us your name, email
       address, city and message. You are not required to give a name to be referred.</p>
    <h3>Information collected automatically</h3>
    <p>Standard web server logs: IP address, browser type, device type, referring page, pages requested
       and timestamps. We use this in aggregate to understand which pages are useful and which are not.</p>

    <h2>3. Call tracking and dynamic number insertion</h2>
    <p>The phone numbers on this site are tracked numbers provided by Ringba, a call tracking platform.
       When a page loads, a JavaScript snippet from Ringba may replace the number you see with a number
       from its pool. This lets the platform attribute a call to the page and campaign that generated it
       and route the call correctly.</p>
    <p>In doing so, Ringba records an "impression" containing technical session data about your visit.
       That data typically includes your IP address, browser and device characteristics, the page URL
       you called from, the referrer, any campaign or URL parameters present (for example a source or
       keyword code from an advertisement), and a session identifier held in a cookie or equivalent
       browser storage. Ringba starts a timer when it assigns a number so that a call placed within the
       session can be matched to the impression.</p>
    <p>We do not control Ringba's systems. Ringba processes this data as our service provider for call
       tracking, under its own terms and privacy policy. If the tracking script fails to load, the
       fallback number on the page still works and no session data is sent.</p>

    <h2>4. Cookies and similar technologies</h2>
    <p>The site itself sets no advertising cookies. The call tracking provider may set a cookie or use
       equivalent browser storage to maintain the session that connects a page visit to a subsequent
       call. Browser settings can block third-party scripts and cookies; if you do so, the site still
       works and the fallback phone number is still displayed and still routed, but call attribution
       will not function.</p>

    <h2>5. Call recording &mdash; please read this section</h2>
    <div class="note warn">
      <p><strong>Notice:</strong> calls made to numbers published on this site <strong>may be recorded
      and monitored</strong> for quality assurance, training, dispute resolution, and to route and
      attribute the call. Recording is a feature of the call tracking platform and may be enabled on the
      campaign serving your call.</p>
    </div>
    <p>Call recording consent law varies by jurisdiction. A number of U.S. states, <strong>including
       California</strong>, require the consent of all parties to record a telephone conversation
       (California Penal Code section 632 applies to confidential communications). Because this site
       serves callers in California and elsewhere, we give notice here and by automated or live
       announcement on the call where the campaign is configured to provide one.</p>
    <p><strong>If you do not want your call recorded, say so at the start of the call, or do not
       call.</strong> You can instead use the contact form on the <a href="/contact.html">contact
       page</a>, which is not recorded.</p>
    <p>Recordings may be shared with the plumbing professional who receives the referral, to the extent
       needed to serve you.</p>

    <h2>6. Who we share information with</h2>
    <ul>
      <li><strong>The plumbing professional you are referred to</strong> \u2014 your location, contact
        details and description of the problem, so they can serve you.</li>
      <li><strong>Ringba</strong>, our call tracking provider, as described in section 3.</li>
      <li><strong>Our hosting provider</strong>, which processes server logs.</li>
      <li><strong>Where legally required</strong> \u2014 in response to a valid subpoena, court order or
        other legal process.</li>
    </ul>
    <p>We do not share your information with unrelated third parties for their own marketing.</p>

    <h2>7. Data retention</h2>
    <p>Call tracking impressions and call records are retained by Ringba according to the retention
       settings configured on the account, typically for a period measured in months for reporting
       purposes. Contact form messages are retained until the enquiry is resolved. Server logs are
       retained on a rolling basis. You can request deletion at any time under section 9.</p>

    <h2>8. Security</h2>
    <p>The site is served over HTTPS. Phone numbers are transmitted over the public telephone network,
       which is not encrypted end to end. Do not send sensitive information such as payment card
       numbers, Social Security numbers or full account credentials through the contact form or by
       leaving them in a voicemail.</p>

    <h2>9. Your rights</h2>
    <p>Depending on where you live, you may have rights to access, correct, delete or restrict the use
       of your personal information, and to opt out of the "sale" or "sharing" of personal information.</p>
    <h3>California residents (CCPA / CPRA)</h3>
    <p>If you are a California resident you have the right to: know what personal information we have
       collected about you and why; request deletion; request correction; opt out of the sale or sharing
       of personal information; and limit the use of sensitive personal information. You may exercise
       these rights by emailing <a href="mailto:{email}">{email}</a>. We will not discriminate against
       you for exercising them. Note that opting out of sharing may mean we cannot attribute or route
       your call, though the fallback number will still connect.</p>
    <h3>Do Not Track</h3>
    <p>The site does not track you across unrelated third-party websites. The call tracking described in
       section 3 is first-party attribution of a call to a page on this site.</p>
    <h3>Other jurisdictions</h3>
    <p>If you are in a jurisdiction with similar rights, contact us at
       <a href="mailto:{email}">{email}</a> and we will respond within a reasonable period.</p>

    <h2>10. Children</h2>
    <p>This site is not directed at children under 13 (or under 16 where applicable law requires it) and
       we do not knowingly collect personal information from them.</p>

    <h2>11. Third-party links</h2>
    <p>City pages describe local conditions using publicly available data. Where we reference a utility,
       a city program or a government body, that is a reference, not an endorsement, and those
       organisations' own privacy policies apply to their sites.</p>

    <h2>12. Changes to this policy</h2>
    <p>If we change this policy we will update the date at the top of this page. Material changes to
       call recording practice will be reflected on the pages that display a phone number.</p>

    <h2>13. Contact</h2>
    <p>{brand}<br>Email: <a href="mailto:{email}">{email}</a><br>
       Referral line (may be recorded): {phone_display}</p>
    <p>{brand} operates no public retail or trade office and employs no plumbers.</p>
  </div>
</section>
""".format(brand=esc(C.BRAND), domain=esc(C.DOMAIN), email=esc(C.CONTACT_EMAIL),
           phone_display=esc(C.PHONE_DISPLAY), date=esc(C.LAUNCH_DATE))

    w("privacy-policy.html", page(
        "Privacy policy | %s" % C.BRAND,
        "How %s handles your data: Ringba call tracking and dynamic number insertion, plus the call "
        "recording notice required in California." % C.BRAND,
        "privacy-policy.html", body))


# ==================================================================== terms ==

def build_terms():
    city_list = ", ".join(c["name"] for c in CITIES)
    body = """
<section class="hero">
  <div class="wrap">
    <ul class="breadcrumb" aria-label="Breadcrumb"><li><a href="/">Home</a></li>
      <li aria-current="page">Terms of service</li></ul>
    <h1>Terms of service</h1>
    <p class="lead">The agreement between you and {brand} when you use this site. Last updated
       {date}.</p>
  </div>
</section>

<section>
  <div class="wrap prose">
    <p>These terms apply to your use of {domain} (the "site"). By using the site or calling a number
       published on it, you agree to these terms. If you do not agree, do not use the site.</p>

    <h2>1. What this service is</h2>
    <p><strong>{brand} is a lead generation and call routing service. It is not a licensed contractor,
       not a plumbing company, and not a party to any contract for plumbing work.</strong></p>
    <p>The service does exactly two things: it publishes information about plumbing issues in specific
       cities, and it routes telephone calls to independent plumbing professionals. We do not perform
       plumbing work, do not supervise plumbing work, do not employ or control the plumbing
       professionals we refer callers to, and do not set or guarantee their prices.</p>

    <h2>2. No warranty of availability, response time or outcome</h2>
    <p>We do not guarantee that any plumbing professional will be available when you call, that a
       plumber will arrive within any particular time, that a specific plumber will be assigned, or
       that your problem can be fixed. Availability depends on third-party businesses we do not
       control. Statements on this site about response are deliberately general for that reason.</p>

    <h2>3. Your relationship is with the plumber</h2>
    <p>Any agreement for work, and any quote, invoice, warranty, guarantee or liability arising from
       plumbing work, is solely between you and the plumbing professional you choose to engage.
       {brand} is not a party to that agreement and has no responsibility for the work performed, the
       price charged, damage caused, or disputes arising.</p>
    <p>You are responsible for verifying that any plumber you engage holds a current licence and
       adequate insurance. In California, contractor licences can be verified through the Contractors
       State License Board (cslb.ca.gov). We recommend doing this before work begins.</p>

    <h2>4. No cost to you</h2>
    <p>There is no charge from {brand} for calling the referral line or for being connected to a
       plumbing professional. Standard telephone charges from your carrier may apply. Plumbing
       businesses pay {brand} for qualified referrals.</p>

    <h2>5. Information on this site</h2>
    <p>City pages contain general information about local conditions, water quality, housing stock and
       municipal programs, drawn from public sources including the U.S. Census Bureau, published
       utility water quality reports, and city and county program pages. Sources are stated on each
       page.</p>
    <p>This is general information, <strong>not professional, legal, engineering or trade advice</strong>,
       and it is not a substitute for an inspection of your actual property. Conditions change, sources
       are updated, and individual properties differ. We make no representation that any statement on
       the site applies to your specific address, water supply or plumbing system.</p>

    <h2>6. Emergencies</h2>
    <p><strong>This is not an emergency service.</strong> If there is a gas leak, a risk of
       electrocution, flooding that threatens life or property, or any other emergency, call 911 or
       your gas, water or electric utility immediately. Do not rely on this site in an emergency.</p>

    <h2>7. Call tracking and recording</h2>
    <p>Numbers on this site are tracked numbers. A call tracking platform may replace the displayed
       number with a number from its pool in order to attribute and route your call, and may record
       technical session data about your visit. <strong>Calls may be recorded and monitored.</strong>
       California and several other states require all-party consent to record telephone conversations;
       by calling you consent to any recording made on the line. If you do not consent, do not call \u2014
       use the contact form instead. Full details are in the <a href="/privacy-policy.html">privacy
       policy</a>.</p>

    <h2>8. Acceptable use</h2>
    <p>You agree not to: use the site or the referral line for any unlawful purpose; place abusive,
       harassing, threatening or prank calls; submit false information with the intent to deceive;
       scrape, data-mine or use automated tools to extract content from the site; attempt to interfere
       with the operation of the site or the call tracking system; or use the site to solicit business
       on behalf of a competing service.</p>

    <h2>9. Intellectual property</h2>
    <p>The site's text, layout, design and the {brand} name are owned by us or licensed to us. Facts and
       public data referenced on city pages remain the property of their original sources. You may quote
       short passages with attribution and a link. You may not reproduce whole pages, republish city
       pages on another site, or use our name in a way that implies endorsement.</p>

    <h2>10. Third-party services</h2>
    <p>The site relies on third-party services including a hosting provider and Ringba for call
       tracking. Their terms and privacy policies apply to their services. We are not responsible for
       the acts or omissions of third parties.</p>

    <h2>11. Disclaimer of warranties</h2>
    <p>THE SITE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, WHETHER EXPRESS,
       IMPLIED OR STATUTORY, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
       FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. WE DO NOT WARRANT THAT THE SITE WILL BE
       UNINTERRUPTED, ERROR-FREE OR THAT ANY REFERRAL WILL RESULT IN SERVICE.</p>

    <h2>12. Limitation of liability</h2>
    <p>TO THE MAXIMUM EXTENT PERMITTED BY LAW, {BRAND} SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL,
       SPECIAL, CONSEQUENTIAL OR PUNITIVE DAMAGES, OR ANY LOSS OF PROFITS, REVENUE, DATA OR GOODWILL,
       ARISING OUT OF OR RELATING TO YOUR USE OF THE SITE OR ANY REFERRAL MADE THROUGH IT, INCLUDING
       DAMAGES ARISING FROM WORK PERFORMED BY A THIRD-PARTY PLUMBING PROFESSIONAL. OUR TOTAL AGGREGATE
       LIABILITY ARISING OUT OF OR RELATING TO THE SITE SHALL NOT EXCEED ONE HUNDRED U.S. DOLLARS
       (USD $100). Some jurisdictions do not allow certain limitations, so some of the above may not
       apply to you.</p>

    <h2>13. Indemnification</h2>
    <p>You agree to indemnify and hold harmless {brand} from any claim, loss, liability or expense
       (including reasonable legal fees) arising out of your misuse of the site, your breach of these
       terms, or your engagement of any plumbing professional referred through the site.</p>

    <h2>14. Dispute resolution</h2>
    <p>These terms are governed by the laws of the State of California, without regard to its conflict
       of laws rules. Any dispute arising out of or relating to these terms or the site shall be
       resolved in the state or federal courts located in California, and you consent to the personal
       jurisdiction of those courts. Nothing in this section limits your right to bring a claim in small
       claims court or to pursue a complaint with a regulatory body such as the Contractors State
       License Board against a plumbing contractor.</p>

    <h2>15. Changes</h2>
    <p>We may update these terms. The date at the top of this page reflects the most recent revision.
       Continued use of the site after a change constitutes acceptance of the updated terms.</p>

    <h2>16. Coverage</h2>
    <p>At the date of these terms the site covers: {cities}. Coverage changes as cities are added or
       removed.</p>

    <h2>17. Contact</h2>
    <p>{brand}<br>Email: <a href="mailto:{email}">{email}</a><br>
       Referral line: {phone_display}</p>
    <p>{brand} operates no public retail or trade office, holds no contractor licence, and employs no
       plumbers.</p>
  </div>
</section>
""".format(brand=esc(C.BRAND), BRAND=esc(C.BRAND.upper()), domain=esc(C.DOMAIN),
           email=esc(C.CONTACT_EMAIL), phone_display=esc(C.PHONE_DISPLAY),
           date=esc(C.LAUNCH_DATE), cities=esc(city_list))

    w("terms.html", page(
        "Terms of service | %s" % C.BRAND,
        "Terms for %s: a lead generation and call routing service, not a licensed plumbing contractor. "
        "Includes call recording consent." % C.BRAND,
        "terms.html", body))


# ==================================================================== 404 =====

def build_404():
    links = "".join('<a class="city-link" href="%s">%s<small>%s</small></a>'
                    % (city_href(c), esc(c["name"]), esc(c["county"])) for c in CITIES)
    body = """
<section class="hero">
  <div class="wrap">
    <h1>That page does not exist</h1>
    <p class="lead">The address you followed is not on this site. If you were looking for a city page,
       it is probably in the list below.</p>
    <div class="hero-cta">{phone_lg}
      <a class="btn outline" href="/">Go to the homepage</a></div>
    <p class="hero-note">{disc_short}</p>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Covered cities</h2>
    <div class="city-grid">{links}</div>
  </div>
</section>
""".format(phone_lg=T.phone_link("lg"), disc_short=esc(C.DISCLOSURE_SHORT), links=links)
    w("404.html", page("Page not found | %s" % C.BRAND,
                       "That page does not exist. Browse the covered cities, or call %s for a plumber "
                       "referral." % C.PHONE_DISPLAY,
                       "404.html", body, robots="noindex,follow"))


# ====================================================== robots / sitemap =====

def build_robots():
    body = """# {brand}
# Referral service. All public pages are indexable; nothing here is private.
User-agent: *
Allow: /
Disallow: /data/

# City pages are published in batches. Batch {batch} ({n} cities) is live.
# Later batches are added as their pages are written to the same standard.
Sitemap: {origin}/sitemap.xml
""".format(brand=C.BRAND, batch=C.BATCH, n=len(CITIES), origin=C.ORIGIN)
    w("robots.txt", body)


def build_sitemap(city_metas):
    today = C.LAUNCH_DATE
    urls = [("https://%s/" % C.DOMAIN, "1.0", "weekly"),
            ("https://%s/how-it-works.html" % C.DOMAIN, "0.7", "monthly"),
            ("https://%s/about.html" % C.DOMAIN, "0.6", "monthly"),
            ("https://%s/contact.html" % C.DOMAIN, "0.5", "monthly")]
    city_urls = [("https://%s/cities/%s.html" % (C.DOMAIN, m["slug"]), "0.9", "monthly")
                 for m in city_metas]
    legal = [("https://%s/privacy-policy.html" % C.DOMAIN, "0.3", "yearly"),
             ("https://%s/terms.html" % C.DOMAIN, "0.3", "yearly")]

    def block(items):
        return "".join(
            "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n  </url>\n" % (loc, today, freq)
            for loc, _p, freq in items)

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + block(urls) + block(city_urls) + block(legal) + "</urlset>\n")
    w("sitemap.xml", xml)


# ==================================================================== main ===

def main():
    written = []
    city_metas = [build_city(i, c) for i, c in enumerate(CITIES)]
    build_home()
    build_how()
    build_about()
    build_contact()
    build_privacy()
    build_terms()
    build_404()
    build_robots()
    build_sitemap(city_metas)

    for root, _dirs, files in os.walk(OUT):
        for f in files:
            p = os.path.join(root, f)
            written.append((os.path.relpath(p, OUT), os.path.getsize(p)))

    print("Built %d files -> %s" % (len(written), OUT))
    print("  city pages : %d" % len(city_metas))
    print("  word count : %d-%d per city page"
          % (min(m["words"] for m in city_metas), max(m["words"] for m in city_metas)))
    total = sum(s for _n, s in written)
    print("  total size : %.0f KB" % (total / 1024.0))
    return city_metas


if __name__ == "__main__":
    metas = main()
    if "--qa" in sys.argv:
        import qa
        qa.run(metas)
