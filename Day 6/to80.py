import argparse

parser = argparse.ArgumentParser('Provide lanternfish data file path')
parser.add_argument('lanternfish', help='A path to a file with lanternfish data')

args = parser.parse_args()

class Lanternfish:
    age = 8

    def __init__(self, age=None):
        if age != None:
            self.age = age
        #if self.age == 8:
        #    print('Hello! I\'m new.')

    def __str__(self):
        return 'Age: ' + str(self.age)

class School:
    school = []

    def __str__(self):
        ages = []
        for fish in self.school:
            ages.append(fish.age)
        return ','.join([str(x) for x in ages])

    def spawn(self, fish):
        self.school.append(fish)

    def age_school(self, days=1, display=True):
        if(display):
            print('Day 0','-',str(self))
        for day in range(1, days + 1):
            
            for i in range(0,len(self.school)):
                fish = self.school[i]
                if fish.age == 0:
                    fish.age = 6
                    self.spawn(Lanternfish(8)) # this is a hack to make the lanternfish age 8 on the next day
                else:
                    # remove a day from every other fish...        
                    fish.age = fish.age - 1 
            if(display): 
                print('Day',day,'-',str(self))

def parse_data(raw_fish_data, school):
    for found_fish_age in raw_fish_data.split(','):
        school.spawn(Lanternfish(age=int(found_fish_age)))

raw_fish_data = ''
school = School()

with open(args.lanternfish, 'r') as file:
    raw_fish_data = file.read().strip()

parse_data(raw_fish_data, school)

#print(school)

school.age_school(days=18, display=False)

#test_18_days = '6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8'

#print(school)
#print(test_18_days)

#test_worked = (str(school) == str(test_18_days))

#print('Test worked?', test_worked)

print('After 18 days there are:', len(school.school), 'fish')

# add another 62 days 
school.age_school(days=62, display=False)

print('After 80 days there are:', len(school.school), 'fish')

