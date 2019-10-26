pragma solidity ^0.5.0;

contract GHC {
    struct Prescription{
        string name;
        string company;
        uint dose;
        string unit;
        string period;
        uint duration;
    }

    struct Doctor{
        string name;
        string hospital;
        uint npat;
        string specialization;
        mapping(uint => address) patients;
        mapping(address => bool) checkpatients;
    }

    struct Patient{
        string name;
        uint age;
        string bloodgroup;
        uint ndoc;
        uint npres;
        mapping(uint => Prescription) prescriptions;
        mapping(uint => address) doctors;
        mapping(address => bool) checkdoctors;
    }

    uint public pid = 0;

    mapping(address => Patient) public allpatients;
    mapping(address => Doctor) public alldoctors;
    mapping(address => bool) public cp;
    mapping(address => bool) public cd;

    function initdoc (
        string memory name,
        string memory hospital,
        string memory specialization
        ) public {
        alldoctors[msg.sender] = Doctor(name, hospital, 0, specialization);
        cd[msg.sender] = true;
    }

    function initpat (
        string memory name,
        uint age,
        string memory bloodgroup
        ) public {
        allpatients[msg.sender] = Patient(name, age, bloodgroup, 0, 0);
        cp[msg.sender] = true;
    }

    function addPrescriptions(
        uint pattt,
        string memory n,
        string memory c,
        uint dos,
        string memory u,
        string memory pe,
        uint dur
        ) public {
        address patientaddr = address(uint(pattt));
        require(cd[msg.sender], "Register as doctor");
        require(cp[patientaddr], "Not a registered patient");
        uint p = allpatients[patientaddr].npres;
        allpatients[patientaddr].prescriptions[p].name = n;
        allpatients[patientaddr].prescriptions[p].company = c;
        allpatients[patientaddr].prescriptions[p].dose = dos;
        allpatients[patientaddr].prescriptions[p].unit = u;
        allpatients[patientaddr].prescriptions[p].period = pe;
        allpatients[patientaddr].prescriptions[p].duration = dur;
        allpatients[patientaddr].npres++;
        if(!allpatients[patientaddr].checkdoctors[msg.sender])
        {
            uint d = allpatients[patientaddr].ndoc;
            allpatients[patientaddr].checkdoctors[msg.sender] = true;
            allpatients[patientaddr].doctors[d] = msg.sender;
            allpatients[patientaddr].ndoc++;
        }
        if(!alldoctors[msg.sender].checkpatients[patientaddr])
        {
            uint d = alldoctors[msg.sender].npat;
            alldoctors[msg.sender].checkpatients[patientaddr];
            alldoctors[msg.sender].patients[d] = patientaddr;
            alldoctors[msg.sender].npat++;
        }
    }
}