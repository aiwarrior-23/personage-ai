import React, { Fragment, useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Breadcrumbs, Btn, H6 } from "../../AbstractElements";
import {
  Button,
  Card,
  CardBody,
  Col,
  Container,
  Form,
  FormGroup,
  input,
  Label,
  Row,
} from "reactstrap";
import { OnboardingUsers } from "../../api_handler/onbordUsers";

const CreateUsers = () => {
  const [formdata, setFormdata] = useState({});
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  useEffect(() => {
    console.log(formdata);
  }, [formdata]);

  const onSubmit = (data) => {
    setFormdata(data);
    OnboardingUsers(data).then((res) => {
      console.log(res);
    });
  };
  return (
    <Fragment>
      <Breadcrumbs
        parent="Users"
        title="Onboarding Users"
        subParent="Profile"
        mainTitle="Onboarding Users"
      />
      <Container fluid={true}>
        <Card>
          <CardBody>
            <Form
              onSubmit={handleSubmit(onSubmit)}
              className="form-bookmark needs-validation"
            >
              <H6>Create Users</H6>
              <Row>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">User Name</Label>
                    <input
                      className={`form-control ${
                        errors.username && "is-invalid"
                      }`}
                      type="text"
                      placeholder="your Name"
                      name="username"
                      defaultValue={formdata.username || ""}
                      {...register("username", { required: true })}
                    />
                    <span className="text-danger">
                      {errors.username && "User name is required"}
                    </span>
                  </FormGroup>
                </Col>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">FirstName</Label>
                    <input
                      className={`form-control ${
                        errors.firstname && "is-invalid"
                      }`}
                      type="text"
                      placeholder="First Name"
                      name="firstname"
                      defaultValue={formdata.firstname || ""}
                      {...register("firstname", { required: true })}
                    />
                    <span className="text-danger">
                      {errors.firstname && "First name is required"}
                    </span>
                  </FormGroup>
                </Col>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">LastName</Label>
                    <input
                      className={`form-control ${
                        errors.lastname && "is-invalid"
                      }`}
                      type="text"
                      placeholder="Last Name"
                      name="lastname"
                      defaultValue={formdata.lastname || ""}
                      {...register("lastname", { required: true })}
                    />
                    <span className="text-danger">
                      {errors.lastname && "Last name is required"}
                    </span>
                  </FormGroup>
                </Col>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">Email</Label>
                    <input
                      className={`form-control ${errors.email && "is-invalid"}`}
                      type="email"
                      placeholder="Email Address"
                      name="email"
                      defaultValue={formdata.email || ""}
                      {...register("email", { required: true })}
                    />
                    <span className="text-danger">
                      {errors.email && "Email is required"}
                    </span>
                  </FormGroup>
                </Col>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">company name</Label>
                    <input
                      className={`form-control ${
                        errors.company && "is-invalid"
                      }`}
                      type="text"
                      placeholder="Company Name"
                      name="company"
                      defaultValue={formdata.company || ""}
                      {...register("company", { required: true })}
                    />
                    <span className="text-danger">
                      {errors.company && "Company is required"}
                    </span>
                  </FormGroup>
                </Col>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">User Type</Label>
                    <select
                      className={`form-control ${
                        errors.userType && "is-invalid"
                      }`}
                      name="userType"
                      defaultValue={formdata.userType || ""}
                      {...register("userType", { required: true })}
                    >
                      <option value="">select</option>
                      <option value="Admin">Admin</option>
                      <option value={"Manager"}>Manager</option>
                      <option value={"Employee-Interviewer"}>
                        Employee-Interviewer
                      </option>
                      <option value={"Employee-HR"}>Employee-Hr</option>
                    </select>
                    <span className="text-danger">
                      {errors.userType && "UserType is required"}
                    </span>
                  </FormGroup>
                </Col>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">Location</Label>
                    <input
                      className={`form-control ${
                        errors.location && "is-invalid"
                      }`}
                      type="text"
                      placeholder="Location"
                      name="location"
                      defaultValue={formdata.location || ""}
                      {...register("location", { required: true })}
                    />
                    <span className="text-danger">
                      {errors.location && "Location is required"}
                    </span>
                  </FormGroup>
                </Col>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">Department</Label>
                    <select
                      className={`form-control ${
                        errors.department && "is-invalid"
                      }`}
                      name="department"
                      defaultValue={formdata.department || ""}
                      {...register("department", { required: true })}
                    >
                      <option>select</option>
                      <option value={"HR"}>HR</option>
                      <option value={"IT-Machine Leaning"}>
                        IT-Machine Leaning
                      </option>
                      <option value={"IT-Web Development"}>
                        IT-Web Development
                      </option>
                      <option value={"IT-App Development"}>
                        IT-App Development
                      </option>
                    </select>
                    <span className="text-danger">
                      {errors.department && "Department is required"}
                    </span>
                  </FormGroup>
                </Col>
                <Col sm="6">
                  <FormGroup>
                    <Label className="col-form-label">Reporting Manager</Label>
                    <select
                      className={`form-control ${
                        errors.reporting_manager && "is-invalid"
                      }`}
                      name="reporting_manager"
                      defaultValue={formdata.reporting_manager || ""}
                      {...register("reporting_manager", { required: true })}
                    >
                      <option>select</option>
                      <option value={"Sandip"}>Sandip</option>
                      <option value={"Shubham"}>Shubham</option>
                      <option value={"Himanshu"}>Himanshu</option>
                    </select>
                    <span className="text-danger">
                      {errors.reporting_manager &&
                        "Reporting Manager is required"}
                    </span>
                  </FormGroup>
                </Col>
              </Row>
              <div className="text-end btn-mb">
                <Button color="primary" type="submit">
                  Submit
                </Button>
              </div>
            </Form>
          </CardBody>
        </Card>
      </Container>
    </Fragment>
  );
};

export default CreateUsers;
