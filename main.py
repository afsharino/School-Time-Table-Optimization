import copy
import random
from collections import deque

class Timetable:
    def __init__(self, schedule, time_slots, days):
        self.schedule = schedule
        self.time_slots = time_slots
        self.days = days
        self.assignment = {'6th': [], '7th': [], '8th': []}
        self.available_slots = {'6th': [(day, time_slot) for day in days for time_slot in time_slots],
                                '7th': [(day, time_slot) for day in days for time_slot in time_slots],
                                '8th': [(day, time_slot) for day in days for time_slot in time_slots]}
        

    def assign_timeslot(self, teacher_info, grade):
        # Check if there are available slots
        if not self.available_slots[grade]:
            print("No available slots.")
            inp = input()
            #return False

        # Randomly choose from available slots
        day, time_slot = random.choice(self.available_slots[grade])

        # Check if the assignment violates any constraints
        if not self.is_valid_assignment(teacher_info, day, time_slot, grade)[0]:
            print("\n-------------------------------------------------------------------------------")
            print(f"Violation: {teacher_info['teacher']} cannot be assigned to {day} - {time_slot}")
            print(f"Reason: {self.is_valid_assignment(teacher_info, day, time_slot, grade)[1]}")
            print("-------------------------------------------------------------------------------\n")
            return False

        # Assign the timeslot
        assignment_entry = {'teacher': teacher_info['teacher'], 'subject': teacher_info['subject'], 'day': day,
                            'time_slot': time_slot}
        self.assignment[grade].append(assignment_entry)
        print(f"\nAssigned {teacher_info['teacher']} to {day} - {time_slot}\n")

        # Remove the assigned slot from available slots
        self.available_slots[grade].remove((day, time_slot))
        return True

    def is_valid_assignment(self, teacher_info, day, time_slot, grade):
        # Constraint 1: two teacher not to be in same class at the same time
        if self.assignment[grade]:
            for class_info in self.assignment[grade]:
                if class_info['day'] == day and class_info['time_slot'] == time_slot:
                    return False, f"{day} - {time_slot} has been assigned to {class_info['teacher']} before."
        
        # Constraint 2: A theacher not to be in different classes at the same time
        if grade == '7th':
            for class_info in self.assignment['6th']:
                if class_info['teacher'] == teacher_info['teacher'] and class_info['day'] == day and class_info['time_slot'] == time_slot:
                    return False, f"{teacher_info['teacher']} Has class in grade 6th at {day} - {time_slot} ."
        
        if grade == '8th':
            for class_info in self.assignment['6th']:
                if class_info['teacher'] == teacher_info['teacher'] and class_info['day'] == day and class_info['time_slot'] == time_slot:
                    return False, f"{teacher_info['teacher']} Has class in grade 6th at {day} - {time_slot} ."
            
            for class_info in self.assignment['7th']:
                if class_info['teacher'] == teacher_info['teacher'] and class_info['day'] == day and class_info['time_slot'] == time_slot:
                    return False, f"{teacher_info['teacher']} Has class in grade 7th at {day} - {time_slot} ."
        

        return True, None


def generate_timetable(schedule, time_slots, days):
    timetable = Timetable(schedule, time_slots, days)
    print(f"********** Start Generating Primary Timetable **********\n\n")

    

    # Define the required number of times each subject should be taught for each grade
    subject_requirements = {
        '6th': {'Math': 4, 'Literature': 4, 'Counseling': 1, 'Sciences': 3, 'Arabic': 2, 'Religious': 1,
                'English': 2, 'Social-studies': 2, 'Business&Technology': 1},
        '7th': {'Math': 4, 'Literature': 4, 'Counseling': 1, 'Sciences': 3, 'Arabic': 2, 'Religious': 1,
                'English': 2, 'Social-studies': 2, 'Business&Technology': 1},
        '8th': {'Math': 4, 'Literature': 4, 'Counseling': 1, 'Sciences': 3, 'Arabic': 2, 'Religious': 1,
                'English': 2, 'Social-studies': 2, 'Business&Technology': 1}
    }

    # Iterate through each grade
    for grade in subject_requirements.keys():
        print(f"Generating Timetable for {grade} Class...\n\n")
        # Sort teachers based on their work load in descending order
        sorted_teachers = deque(sorted(schedule, key=lambda teacher_info: teacher_info.get('work_load', 0), reverse=True))
        print(f'\n{sorted_teachers}\n')
        filled_courses = []
        teacher_info = {}
        while len(filled_courses) != 9:
            print(f"\nfilled courses: {filled_courses}\n")
            # Update theacher workload
            if teacher_info:
                for teacher in sorted_teachers:
                    if teacher_info['teacher'] == teacher['teacher']:
                        sorted_teachers.append(teacher_info)
                        sorted_teachers.remove(teacher)
                        break

            while True:
                # Sort teachers based on their remaining work load for the specific grade
                #sorted_teachers_grade = deque(sorted(sorted_teachers, key=lambda teacher_info: teacher_info.get('work_load', 0), reverse=True))

                # Check if the teacher's subject for the current grade is already filled
                teacher_info = sorted_teachers[0]
                if teacher_info['subject'] in filled_courses:
                    sorted_teachers.rotate(-1)
 
                else:
                    break

            # the subject that we are filling for grade
            subject = teacher_info['subject']

            # count unit
            units = subject_requirements[grade][subject]

            while units:
                # Assign the teacher to random timeslots for the current grade
                if timetable.assign_timeslot(teacher_info, grade):
                    teacher_info['work_load'] = teacher_info['work_load'] - 1
                    units -= 1
            filled_courses.append(subject)

    return timetable.assignment

def print_timetable(timetable):
    for grade, assignments in timetable.items():
        print(f"\n{72*'*'} Timetable for {grade} Grade {72*'*'}\n")
        print("{:<20}".format("Time Slots"), end="")
        for day in days:
            print("{:<30}".format(day), end="")
        print("\n" + "=" * (20 + 30 * len(days)))

        for time_slot in time_slots:
            print("{:<20}".format(time_slot), end="")
            for day in days:
                assignment = next((assign for assign in assignments if assign['day'] == day and assign['time_slot'] == time_slot), None)
                if assignment:
                    print("{:<30}".format(f"{assignment['teacher']} - {assignment['subject']}"), end="")
                else:
                    print("{:<30}".format("Available"), end="")
            print("\n" + "-" * (20 + 30 * len(days)))

class TimetableOptimization:
    def __init__(self, timetable, days, time_slots):
        self.timetable = timetable
        self.days = days
        self.time_slots = time_slots

    def evaluate_timetable(self, timetable):
        # Initialize scores for each grade
        scores = {'6th': 0, '7th': 0, '8th': 0}

        for grade, assignments in timetable.items():
            teacher_days = {}

            # Count the number of unique days each teacher has classes
            for assignment in assignments:
                teacher = assignment['teacher']
                day = assignment['day']

                if teacher not in teacher_days:
                    teacher_days[teacher] = set()

                teacher_days[teacher].add(day)

            # Calculate the score for each teacher based on the preference
            for teacher, days in teacher_days.items():
                score = len(days)  # The more unique days, the lower the score
                scores[grade] += score

        # Return the total score for the timetable
        total_score = sum(scores.values())
        return total_score

    def apply_move_within_neighborhood(self, timetable):
        # Implement a move operation within the neighborhood
        # For simplicity, let's randomly swap classes for a teacher in the same grade
        modified_timetable = copy.deepcopy(timetable)

        grade = random.choice(list(modified_timetable.keys()))
        teacher = random.choice(list(set(assignment['teacher'] for assignment in modified_timetable[grade])))
        
        # Collect the available slots for the selected teacher in the same grade
        available_teacher_slots = [(day, time_slot) for day in self.days for time_slot in self.time_slots
                                   if (day, time_slot) not in [(assignment['day'], assignment['time_slot']) for assignment in modified_timetable[grade] if assignment['teacher'] == teacher]]
        
        # Randomly choose two different slots
        if len(available_teacher_slots) >= 2:
            slot1, slot2 = random.sample(available_teacher_slots, 2)

            # Swap the classes for the selected teacher
            for assignment in modified_timetable[grade]:
                if assignment['teacher'] == teacher and assignment['day'] == slot1[0] and assignment['time_slot'] == slot1[1]:
                    assignment['day'], assignment['time_slot'] = slot2[0], slot2[1]
                elif assignment['teacher'] == teacher and assignment['day'] == slot2[0] and assignment['time_slot'] == slot2[1]:
                    assignment['day'], assignment['time_slot'] = slot1[0], slot1[1]

        return modified_timetable
    


    def variable_neighborhood_search(self, max_iterations):
        best_timetable = copy.deepcopy(self.timetable)
        best_score = self.evaluate_timetable(best_timetable)
        print(f"\nScore of Primary Timetable is: {best_score}\n")

        current_timetable = copy.deepcopy(self.timetable)
        current_score = best_score

        for iteration in range(max_iterations):
            new_timetable = self.apply_move_within_neighborhood(current_timetable)
            new_score = self.evaluate_timetable(new_timetable)

            if new_score > current_score:
                current_timetable = copy.deepcopy(new_timetable)
                current_score = new_score

                if new_score > best_score:
                    best_timetable = copy.deepcopy(new_timetable)
                    best_score = new_score
                    print(f"\nNew Best Score founded: {best_score}\n")

        return best_timetable
if __name__ == '__main__':
    schedule = [
            {'teacher': 'Afshari', 'subject': 'Counseling', 'work_load': 3},
            {'teacher': 'Khoshbakht', 'subject': 'Sciences', 'work_load': 6},
            {'teacher': 'Tajik', 'subject': 'Literature', 'work_load': 4},
            {'teacher': 'Naghavi', 'subject': 'Arabic', 'work_load': 6},
            {'teacher': 'Tavakoli', 'subject': 'Religious', 'work_load': 3},
            {'teacher': 'Aghavali', 'subject': 'Math', 'work_load': 8},
            {'teacher': 'Mehrafar', 'subject': 'English', 'work_load': 4},
            {'teacher': 'Saberi', 'subject': 'Social-studies', 'work_load': 4},
            {'teacher': 'Asheri', 'subject': 'Business&Technology', 'work_load': 3},
            {'teacher': 'Elyasi', 'subject': 'Sciences', 'work_load': 3},
            {'teacher': 'Rad', 'subject': 'Literature', 'work_load': 8},
            {'teacher': 'Khanmohammadi', 'subject': 'Math', 'work_load': 4},
            {'teacher': 'Mehrafar', 'subject': 'English', 'work_load': 2},
            {'teacher': 'Avarand', 'subject': 'Social-studies', 'work_load': 2},
    ]

    days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday']
    time_slots = ['8:00 AM - 8:45 AM', '9:10 AM - 9:50 AM', '10:15 AM - 11:00 AM', '11:20 AM - 12:10 PM']

    import time
    start_time = time.time()
    result_schedule = generate_timetable(schedule, time_slots, days)
    print("My program took", time.time() - start_time, "to run")

    print_timetable(result_schedule)


     # Initialize TimetableOptimization with the initial timetable
    timetable_optimizer = TimetableOptimization(result_schedule, days, time_slots)

    # Perform Variable Neighborhood Search for optimization
    optimized_timetable = timetable_optimizer.variable_neighborhood_search(max_iterations=100)

    print("\n********** Optimized Timetable **********\n")
    print_timetable(optimized_timetable)
