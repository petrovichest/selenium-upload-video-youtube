class TimeConverter:

    def seconds_to_minutes(self, seconds):
        minutes = seconds // 60
        seconds_without_minutes = seconds % 60
        if len(str(minutes)) < 2:
            minutes = f'0{minutes}'
        if len(str(seconds_without_minutes)) < 2:
            seconds_without_minutes = f'0{seconds_without_minutes}'
        total = f'{minutes}:{seconds_without_minutes}'
        return total

if __name__ == '__main__':
    print(TimeConverter().seconds_to_minutes(seconds=65))