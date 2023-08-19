Chevrons
########

Chevrons 101
============

Chevron Colors
-------------------------

The team chevrons come in three colors, Red, White, and
Gold. Red denotes standard, a baseline color which is
used for active student team members and mentor
chevrons. White denotes Alumnanship, used to reflect a
Alumni's position or creditable actions on the team. 
Finally, Gold denotes senior leadership, Captain and Ast.
Captain positions. 

Chevron Hierarchy
-----------------

Chevrons do not stack, they overlap, This means if you fill
multiple roles, chevrons will overlap in a set hierarchy, and
it is as follows:

A full red bar will replace a half red bar.
A gold bar will replace a red bar
White bars are placed last.

For example, if you had the following two roles:

.. chevron::
   :chevrons: ["none", "none", "red", "red", "none"]
   :patches: [["Mechanical", "red"]]

.. chevron::
   :chevrons: ["none", "none", "red",  "none", "none"]
   :patches: [["Driver", "red"]]

Then your final patch would look like this

..  chevron::
   :chevrons: ["none", "none", "red", "red", "none"]
   :patches: [["Mechanical", "red"], ["Driver", "red"]]


Patch Placement
---------------

The team patches reflect drive team positions, subteam 
denotations for leads, Captain's position, and lead mentor
position. Similar to chevron colors, Red denotes active
work for the patch, and white an Alumni of the position.
Gold denotes senior leadership, and it used for Captain
and asst. captain.

White patches are only given out to Alumni's who've worked
in the position either as lead, or on drive team, or as a
mentor which is worthy of their work being memorialized a
white patch.


Mentor and Alumni Chevrons
==========================

.. chevron::
   :chevrons: ["none", "none", "white", "none", "none"]
   :patches: [["LeadMentor", "red"]]

   Lead mentor's livery.

.. chevron::
   :chevrons: ["none", "red", "white", "none", "none"]

   Mentor Drive Coach's livery.

.. chevron::
   :chevrons: ["none", "none", "gold", "white", "white"]

   Alumni Captain's livery.

.. chevron::
   :chevrons: ["none", "none", ["gold", "white"], "white", "white"]

   Alumni Assistant Captain's livery.

Examples
========

.. chevron::
   :chevrons: ["none", "red", "white", "white", "none"]
   :patches: [["Mechanical", "white"], ["Electrical", "white"]]

   Alumni drive coach who was lead of electrical and lead of mechanical
   during their time as a team member. (Likely not during the same years)

   
.. chevron::
   :chevrons: ["none", "none", "white", "white", "none"]
   :patches: [["Software", "white"], ["Driver", "white"]]

   Alumni member who was lead of code and driver while they were on the team.

.. chevron::
   :chevrons: ["none", "none", "white", "none", "none"]

   A current mentor on the team.
