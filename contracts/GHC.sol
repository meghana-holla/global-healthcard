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
        address id;
        string name;
        string hospital;
        uint npat;
        string specialization;
        mapping(uint => address) patients;
        mapping(address => bool) checkpatients;
    }

    struct Patient{
        address id;
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
        alldoctors[msg.sender] = Doctor(msg.sender, name, hospital, 0, specialization);
        cd[msg.sender] = true;
    }

    function initpat (
        string memory name,
        uint age,
        string memory bloodgroup
        ) public {
        allpatients[msg.sender] = Patient(msg.sender, name, age, bloodgroup, 0, 0);
        cp[msg.sender] = true;
    }

    address public get_pat_return_value;
    function getpat(uint i) public
    {
        address p = alldoctors[msg.sender].patients[i];
        get_pat_return_value = p;
    }

    address public get_doc_return_value;
    function getdoc(uint i) public
    {
        address p = allpatients[msg.sender].doctors[i];
        get_doc_return_value = p;
    }

    Prescription public get_pres_return_value;
    function getpres(uint i) public
    {
        Prescription memory p = allpatients[msg.sender].prescriptions[i];
        get_pres_return_value = p;
    }

    function addPrescriptions(
        uint pat_id,
        string memory name,
        string memory company,
        uint dose,
        string memory unit,
        string memory period,
        uint duration
        ) public {
        address patientaddr = address(uint(pat_id));
        require(cd[msg.sender], "Register as doctor");
        require(cp[patientaddr], "Not a registered patient");
        uint p = allpatients[patientaddr].npres;
        allpatients[patientaddr].prescriptions[p].name = name;
        allpatients[patientaddr].prescriptions[p].company = company;
        allpatients[patientaddr].prescriptions[p].dose = dose;
        allpatients[patientaddr].prescriptions[p].unit = unit;
        allpatients[patientaddr].prescriptions[p].period = period;
        allpatients[patientaddr].prescriptions[p].duration = duration;
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