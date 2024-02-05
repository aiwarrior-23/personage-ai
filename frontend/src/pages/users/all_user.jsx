import React, { Fragment, useCallback, useEffect, useState } from "react";
import { Breadcrumbs, Btn, H4 } from "../../AbstractElements";
import { Card, CardBody, Container } from "reactstrap";
import DataTable from "react-data-table-component";
import { All_user_tableColumns } from "../../Data/Table/Defaultdata";
import { GetAllUsers } from "../../api_handler/onbordUsers";

const GetUsers = () => {
  const [data, setData] = useState([]);

  // const handleRowSelected = useCallback((state) => {
  //   setSelectedRows(state.selectedRows);
  // }, []);

  useEffect(() => {
    GetAllUsers().then((res) => {
      setData(res.data);
    });
    All_user_tableColumns.push({
      name: "Action",
      cell: (row) => (
        <div className="d-flex">
          <Btn
            attrBtn={{
              className: "btn-icon",
              color: "primary",
              size: "sm",
              onClick: () => {
                console.log(row);
              },
            }}
          >
            <i className="fa fa-pencil"></i>
            Edit
          </Btn>
          <Btn
            attrBtn={{
              className: "btn-icon",
              color: "danger",
              size: "sm",
              onClick: () => {
                console.log(row);
              },
            }}
          >
            <i className="fa fa-trash"></i>
            Delete
          </Btn>
        </div>
      ),
    });
  }, []);

  return (
    <Fragment>
      <Breadcrumbs
        parent="Users"
        title="All Users"
        subParent="Profile"
        mainTitle="All Users"
      />
      <Container fluid={true}>
        <Card>
          <CardBody>
            <DataTable
              data={data}
              columns={All_user_tableColumns}
              striped={true}
              center={true}
              pagination
            />
          </CardBody>
        </Card>
      </Container>
    </Fragment>
  );
};
export default GetUsers;
