from rest_framework import serializers
from emsmodel import models


class dummySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.dummy
        fields = '__all__'
        # exclude = ['id']  # If you want to exclude the primary key field

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        # fields = [
        #     "vid",
        #     "vcode",
        #     "vname",
        #     "vnameurdu",
        #     "address1",
        #     "address2",
        #     "addressurdu1",
        #     "addressurdu2",
        #     "sortorder",
        #     "logo",
        #     "isactive",
        #     #"uid",
        #     #"tranzdatetime",
        # ]
        fields = '__all__'
        #exclude = ['uid',
        #           'tranzdatetime']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'

class DepartmentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DepartmentGroup
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Designation
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = '__all__'

class AllowDedCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AllowDedCat
        fields = '__all__'

class AllowDedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AllowDed
        fields = '__all__'

class AllowDedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AllowDedGroup
        fields = '__all__'

class AttCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttCode
        fields = '__all__'

class AttGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttGroup
        fields = '__all__'

class RamazanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ramazan
        fields = '__all__'

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Holiday
        fields = '__all__'

class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaveBalance
        fields = '__all__'

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttGroup
        # fields = '__all__'
        fields = [
            "vid",
            "vcode",
            "vname"
        ]

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shift
        fields = '__all__'

class SalaryIncrementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SalaryIncrement
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vname'].required = False
        self.fields['vno'].required = False
        self.fields['currentdesgid'].required = False
        self.fields['newdesgid'].required = False
        self.fields['isposted'].required = False
        self.fields['postedby'].required = False
        self.fields['posteddate'].required = False
        self.fields['iscanceled'].required = False

class SalaryAllowDedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SalaryAllowDed
        fields = '__all__'

    def create(self, validated_data):
        last_vno = models.SalaryAllowDed.objects.order_by('-vid').first()
        if last_vno and last_vno.vno:
            last_number = int(last_vno.vno.replace('v-', ''))
        else:
            last_number = 0
        new_number = last_number + 1
        new_code = f'v-{new_number}'

        validated_data['vno'] = new_code
        return super().create(validated_data)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vname'].required = False
        self.fields['vno'].required = False
        self.fields['refno'].required = False
        self.fields['qty'].required = False
        self.fields['isapproved'].required = False
        self.fields['approvedby'].required = False
        self.fields['approveddate'].required = False
        self.fields['isposted'].required = False
        self.fields['postedby'].required = False
        self.fields['posteddate'].required = False

class SalaryLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SalaryLoan
        fields = '__all__'

    def create(self, validated_data):
        last_vno = models.SalaryLoan.objects.order_by('-vid').first()
        if last_vno and last_vno.vno:
            last_number = int(last_vno.vno.replace('v-', ''))
        else:
            last_number = 0
        new_number = last_number + 1
        new_code = f'v-{new_number}'

        validated_data['vno'] = new_code
        return super().create(validated_data)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vname'].required = False
        self.fields['vno'].required = False
        self.fields['refno'].required = False
        self.fields['usedamount'].required = False
        self.fields['isapproved'].required = False
        self.fields['approvedby'].required = False
        self.fields['approveddate'].required = False
        self.fields['isposted'].required = False
        self.fields['postedby'].required = False
        self.fields['posteddate'].required = False

class SalaryLoanDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SalaryLoanDeduction
        fields = '__all__'

class AttMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttMain
        fields = '__all__'

class AttClosingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttClosingDay
        fields = '__all__'

class AttLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttLeave
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contactnumber'].required = False
        self.fields['shiftid'].required = False
        self.fields['isapproved'].required = False
        self.fields['approvedby'].required = False
        self.fields['approveddate'].required = False
        self.fields['isposted'].required = False
        self.fields['postedby'].required = False
        self.fields['posteddate'].required = False

class AttLeaveSpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttLeaveSpecial
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contactnumber'].required = False
        self.fields['isapproved'].required = False
        self.fields['approvedby'].required = False
        self.fields['approveddate'].required = False
        self.fields['isposted'].required = False
        self.fields['postedby'].required = False
        self.fields['posteddate'].required = False

class AttOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttOT
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vno'].required = False

class AttOTMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttOTMonth
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vno'].required = False

class SalaryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SalaryType
        fields = '__all__'

class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeeType
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gender
        fields = '__all__'

class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Religion
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'

class EmpLocationTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmpLocationTransfer
        fields = '__all__'

    def create(self, validated_data):
        last_vno = models.EmpLocationTransfer.objects.order_by('-VID').first()
        if last_vno and last_vno.vno:
            last_number = int(last_vno.vno.replace('v-', ''))
        else:
            last_number = 0
        new_number = last_number + 1
        new_code = f'v-{new_number}'

        validated_data['vno'] = new_code
        return super().create(validated_data)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vno'].required = False

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'

    def create(self, validated_data):
        last_emp = models.Employee.objects.order_by('-empid').first()
        if last_emp and last_emp.empcode:
            last_number = int(last_emp.empcode.replace('emp', ''))
        else:
            last_number = 0
        new_number = last_number + 1
        new_emp_code = f'emp{new_number:03d}'  # emp001, emp002

        validated_data['empcode'] = new_emp_code
        return super().create(validated_data)

    def to_internal_value(self, data):
        if 'dojact' in data and data['dojact'] == '':
            data['dojact'] = '1900-01-01'
        
        if 'dol' in data and data['dol'] == '':
            data['dol'] = '1900-01-01'

        if 'dolact' in data and data['dolact'] == '':
            data['dolact'] = '1900-01-01'

        if 'transportdate' in data and data['transportdate'] == '':
            data['transportdate'] = '1900-01-01'

        if 'probitiondate' in data and data['probitiondate'] == '':
            data['probitiondate'] = '1900-01-01'

        if 'pfundentitleddate' in data and data['pfundentitleddate'] == '':
            data['pfundentitleddate'] = '1900-01-01'

        if 'pessidate' in data and data['pessidate'] == '':
            data['pessidate'] = '1900-01-01'

        return super().to_internal_value(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['machinecode'].required = False
        self.fields['hodid'].required = False
        self.fields['dojact'].required = False
        self.fields['actualsalary'].required = False
        self.fields['managersalary'].required = False
        self.fields['replacementof'].required = False
        self.fields['replacementof'].required = False
        self.fields['dol'].required = False
        self.fields['dolact'].required = False
        self.fields['leftremarks'].required = False
        self.fields['cellphone'].required = False
        self.fields['icephone'].required = False
        self.fields['addresspermanent'].required = False
        self.fields['bloodgroup'].required = False
        self.fields['eobino'].required = False
        self.fields['eobinoact'].required = False
        self.fields['ssno'].required = False
        self.fields['lifeinsuranceno'].required = False
        self.fields['pfamount'].required = False
        self.fields['pfamount'].required = False
        self.fields['education'].required = False
        self.fields['enameurdu'].required = False
        self.fields['fnameurdu'].required = False
        self.fields['addressurdu'].required = False
        self.fields['designationtitle'].required = False
        self.fields['oldcode'].required = False
        self.fields['mothername'].required = False
        self.fields['nexttokin'].required = False
        self.fields['transportdate'].required = False
        self.fields['transportroute'].required = False
        self.fields['transportlocation'].required = False
        self.fields['otrate'].required = False
        self.fields['otrateoff'].required = False
        self.fields['otrateoff'].required = False

class SecUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecUser
        fields = '__all__'

class SecRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecRole
        fields = '__all__'

class SecPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecPage
        fields = '__all__'

class SecRolePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecRolePage
        fields = '__all__'

class SecUserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecUserCompany
        fields = '__all__'

class SecUserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecUserLocation
        fields = '__all__'

class SecUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecUserRole
        fields = '__all__'

class SecUserPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecUserPage
        fields = '__all__'

class SalaryGratuitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SalaryGratuity
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vname'].required = False
        self.fields['vno'].required = False
        self.fields['isapproved'].required = False
        self.fields['isposted'].required = False
        self.fields['postedby'].required = False
        self.fields['posteddate'].required = False
        self.fields['chequeno'].required = False
        self.fields['chequedate'].required = False

    def create(self, validated_data):
        last_vno = models.SalaryGratuity.objects.order_by('-VID').first()
        if last_vno and last_vno.vno:
            last_number = int(last_vno.vno.replace('v-', ''))
        else:
            last_number = 0
        new_number = last_number + 1
        new_code = f'v-{new_number}'

        validated_data['vno'] = new_code
        return super().create(validated_data)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vname'].required = False
        self.fields['vno'].required = False
        self.fields['isapproved'].required = False
        self.fields['isposted'].required = False
        self.fields['postedby'].required = False
        self.fields['posteddate'].required = False

class EmployeeTrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeeTrial
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['actualempid'].required = False
        self.fields['empcode'].required = False
        self.fields['empcodeold'].required = False
        self.fields['empidold'].required = False
        self.fields['locationid'].required = False

class AttLeaveDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttLeaveDepartment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['locationid'].required = False

class AttExemptLateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttExemptLate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['locationid'].required = False
        self.fields['isposted'].required = False
        self.fields['postedby'].required = False
        self.fields['posteddate'].required = False
        self.fields['iscancel'].required = False

class AttRosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttRoster
        fields = '__all__'

class AttEntryRosterMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttEntryRosterMonth
        fields = '__all__'