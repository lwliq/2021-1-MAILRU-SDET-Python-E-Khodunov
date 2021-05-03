#!/bin/bash
result=result_bash.txt

#1
echo -e "Общее количество запросов" > $result
cat access.log | wc -l | awk '{print $1}' >> $result

#2
echo -e "\nОбщее количество запросов по типу" >> $result
cat access.log | awk '{gsub(/"/, "", $6); print $6}' | sort | uniq -c | sort -rnk 2 | awk '{printf "%s-%d\n", $2, $1}' >> $result

#3
echo -e "\nТоп 10 самых частых запросов" >> $result
cat access.log | awk '{print $7}' | sort | uniq -c | sort -rnk 1 | head | awk '{print $2,$1}' >> $result

#4
echo -e "\nТоп 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой" >> $result
cat access.log | awk '$9 ~ /4[0-9]{2}$/ {print $1,$7,$9,$10}' | sort -rnk 4 | head -n 5 | awk '{print $2,$3,$4,$1}' >> $result

#5
echo -e "\nТоп 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой" >> $result
cat access.log | awk '$9 ~ /5[0-9]{2}$/ {print $1}' | sort -k 1 | uniq -c | sort -rnk 1 | head -n 5 | awk '{print $2,$1}' >> $result
 
