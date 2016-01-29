cursor = db.timer.aggregate(
   [
     {
       $group:
         {
           _id: { week: { $week: "$dateEntered"}, year: { $year: "$dateEntered" } },
           totalHours: { $sum:  {$divide: [ "$seconds" , 3600 ] } },
           count: { $sum: 1 }
         }
     }
   ]
)

while(cursor.hasNext() ) {
  printjson(cursor.next());
}