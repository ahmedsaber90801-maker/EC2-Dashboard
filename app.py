from flask import Flask, render_template, redirect, url_for
import boto3

app = Flask(__name__)

# إنشاء EC2 client
ec2 = boto3.client('ec2', region_name='us-east-1')  # خلي الـ region زي اللي حاطه في credentials

# دالة لجلب كل الـ Instances
def get_instances():
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance['InstanceId'],
                'State': instance['State']['Name'],
                'Type': instance['InstanceType'],
                'PublicIP': instance.get('PublicIpAddress', 'N/A')
            })
    return instances

# الصفحة الرئيسية
@app.route("/")
def index():
    instances = get_instances()
    return render_template("index.html", instances=instances)

# Route لتشغيل Instance
@app.route("/start/<instance_id>")
def start_instance(instance_id):
    try:
        ec2.start_instances(InstanceIds=[instance_id])
    except Exception as e:
        print(f"Error starting instance {instance_id}: {e}")
    return redirect(url_for('index'))

# Route لإيقاف Instance
@app.route("/stop/<instance_id>")
def stop_instance(instance_id):
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
    except Exception as e:
        print(f"Error stopping instance {instance_id}: {e}")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

