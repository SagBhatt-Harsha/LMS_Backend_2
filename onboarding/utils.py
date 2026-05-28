def generate_batch_code(batch_name):

    words = batch_name.split()
    code = ''

    for word in words:
        if word.isdigit():
            code += word

        else:
            code += word[0].upper()
    return code


def generate_roll_number(trainee, batch):

    parts = trainee.registration_code.split('/')
    registration_prefix = f"{parts[0]}/{parts[1]}"

    batch_code = generate_batch_code(batch.name)
    trainee_count = batch.trainees.count()

    roll_number = (f"{registration_prefix}/"f"{batch_code}/"f"{trainee_count:03d}")
    return roll_number