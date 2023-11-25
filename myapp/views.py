from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Import User model
from .forms import CSVUploadForm
from .models import CustomerDetails
import pandas as pd
from django.http import HttpResponse

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # df = pd.read_csv(csv_file, header=0)
            df = pd.read_csv(csv_file, header=0)

            
            # Specify the 'email' column when reading the CSV file
            # df = pd.read_csv(csv_file)
            # print(df.columns)

            # Remove duplicates based on 'email'
            df.drop_duplicates(subset=['email'], keep='first', inplace=True)
            

            for index, row in df.iterrows():
                # Use get_or_create with the User model
                user, created = User.objects.get_or_create(
                    # email='example@email.com',
                    # email='sudhanshu@gmail.com',
                    # email='shreeram0@gmail.com',
                    # email='krishna1@gmail.com',
                    # email='shiv2@gmail.com',
                    email=row['email'],
                    defaults={
                        # 'username': 'example@email.com',
                        # 'username': row['email'],
                        'first_name': row['firstname'],
                        'last_name': row['lastname'],
                        'email':row['email'],
                    }

                )    
                print(user.email)  # Prints 'example@email.com'
                
                    # Querying for a User by email
                existing_user = User.objects.get(email='example@email.com')

                    # Modifying the email attribute
                existing_user.email = 'new_email@example.com'
                existing_user.save()
                

                # CustomerDetails.objects.create(
                #     user=user,
                #     phone_no=row['phone no'],
                #     gender=row['gender'],
                #     dob=row['dob'],
                #     address1=row['address1'],
                #     address2=row['address2'],
                #     pincode=row['pincode'],
                #     state=row['state'],
                #     country=row['country']
                # )


                customer, created = CustomerDetails.objects.get_or_create(
                    email=row['email'],
                    defaults={
    
                        'phone_no': row['phone no'],
                        'gender': row['gender'],
                        'dob': row['dob'],
                        'address1': row['address1'],
                        'address2': row['address2'],
                        'pincode': row['pincode'],
                        'state': row['state'],
                        'country': row['country'],
                    
                    }
                )

            return redirect('display_data')

    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})


def display_data(request):
    customers = CustomerDetails.objects.all()
    return render(request, 'display_data.html', {'customers': customers})


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_data.csv"'

    # Use pandas to export data to CSV
    df = pd.DataFrame(list(CustomerDetails.objects.values()))
    df.to_csv(path_or_buf=response, index=False)

    return response
