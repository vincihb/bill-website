# Credit: https://www.legion.org/legislative/thomas/7153/part-3-kinds-bills

# A bill is a legislative proposal before Congress. Bills from each chamber are assigned a number in the order in which
# they are introduced, starting at the beginning of each Congress (first and second sessions). Often, a member of
# Congress introduces a particular bill annually and will arrange with the chamber's leadership to reserve a certain
# bill number.
#
# Public bills pertain to matters that affect the general public or classes of citizens, while private bills pertain to
# individual matters that affect individuals and organizations, such as claims against the federal government (private
# bills are not as prevalent as they once were).
BILL_TYPES = ['hr', 's']

# A joint resolution is a legislative proposal that requires the approval of both chambers and the signature
# of the president, just as a bill does. Resolutions from each chamber are assigned a number in the order in which
# they are introduced, starting at the beginning of each Congress (first and second sessions).
#
# There is no real difference between a bill and a joint resolution, which is generally used for limited matters,
# such as a single appropriation for a specific purpose. A joint resolution has the force of law, if approved.
JOINT_RESOLUTIONS = ['hjres', 'sjres']

# A concurrent resolution is a legislative proposal that requires the approval of both chambers,
# but does not require the signature of the president and does not have the force of law.
#
# Concurrent resolutions generally are used to make or amend rules that apply to both chambers.
# They are also used to express the sentiments of both chambers.
CONCURRENT_RESOLUTIONS = ['hconres', 'sconres']

# A simple resolution is a legislative proposal that addresses matters entirely within the prerogative of one chamber
# or the other. It requires no approval from the other chamber, or the signature of the president.
# It does not have the force of law.
#
# Most simple resolutions concern the rules or sentiments of one chamber.
SIMPLE_RESOLUTIONS = ['hres', 'sres']