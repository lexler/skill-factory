# Structurizr DSL

Architecture as code. Define the model once, generate multiple views. Render at structurizr.com/dsl or run locally.

These illustrate the syntax. Consider what fits your context.

## Workspace Structure

```
workspace "Name" "Description" {

    model {
        // define people, systems, containers, components, relationships
    }

    views {
        // define which diagrams to generate from the model
    }
}
```

The model defines elements and relationships. Views select what to show in each diagram. This separation means you model once and create multiple views of the same architecture.

## Model Elements

### People and Software Systems

```
person <name> [description] [tags]
softwareSystem <name> [description] [tags] {
    // containers go here
}
```

Assign to variables for referencing in relationships and views:

```
user = person "Customer" "A customer of the bank"
bankSystem = softwareSystem "Internet Banking System" "Allows customers to manage accounts" {
    webapp = container "Web Application" "Serves the SPA" "Java/Spring Boot"
    spa = container "Single-Page App" "Banking UI" "React"
    api = container "API" "Banking API" "Java/Spring Boot"
    db = container "Database" "Stores account data" "PostgreSQL" "database"
}
mainframe = softwareSystem "Mainframe Banking System" "Core banking" "existing"
email = softwareSystem "E-mail System" "Sends emails" "existing"
```

### Containers and Components

```
container <name> [description] [technology] [tags] {
    // components go here
}
component <name> [description] [technology] [tags]
```

### Tags

Tags control styling. Built-in tags: `Element`, `Person`, `Software System`, `Container`, `Component`, `Relationship`. Add custom tags:

```
db = container "Database" "Stores data" "PostgreSQL" "database"
mainframe = softwareSystem "Mainframe" "Legacy system" "existing"
```

## Relationships

```
source -> destination [description] [technology] [tags]
```

Within an element's scope, the source is implicit:

```
user = person "User" {
    -> webapp "Views pages using" "HTTPS"
    -> spa "Interacts with"
}
```

Between named elements:

```
spa -> api "Makes API calls to" "JSON/HTTPS"
api -> db "Reads from and writes to" "JDBC"
api -> mainframe "Gets account info from" "XML/HTTPS"
api -> email "Sends email using" "SMTP"
```

## Views

### System Context

```
views {
    systemContext bankSystem "Context" "System Context diagram" {
        include *
        autoLayout
    }
}
```

### Container

```
    container bankSystem "Containers" "Container diagram" {
        include *
        autoLayout
    }
```

### Component

```
    component api "Components" "API Component diagram" {
        include *
        autoLayout
    }
```

### System Landscape

```
    systemLandscape "Landscape" "All systems" {
        include *
        autoLayout
    }
```

### Dynamic

```
    dynamic bankSystem "SignIn" "Sign-in flow" {
        user -> spa "Opens in browser"
        spa -> api "Sends credentials to"
        api -> db "Validates against"
        api -> spa "Returns auth token to"
    }
```

### Deployment

```
    deployment bankSystem "Production" "Prod" "Production deployment" {
        include *
        autoLayout
    }
```

## Deployment Model

```
model {
    prodEnv = deploymentEnvironment "Production" {
        deploymentNode "AWS" "" "Amazon Web Services" {
            deploymentNode "ECS Cluster" "" "Amazon ECS" {
                containerInstance api
                containerInstance webapp
            }
            deploymentNode "RDS" "" "Amazon RDS" {
                containerInstance db
            }
        }
    }
}
```

## Styling

```
views {
    styles {
        element "Person" {
            shape Person
            background #08427B
            color #ffffff
        }
        element "Software System" {
            background #1168BD
            color #ffffff
        }
        element "Container" {
            background #438DD5
            color #ffffff
        }
        element "database" {
            shape Cylinder
        }
        element "existing" {
            background #999999
        }
        relationship "Relationship" {
            color #707070
            thickness 2
        }
    }
}
```

Available shapes: `Box`, `Circle`, `Cylinder`, `Ellipse`, `Hexagon`, `Person`, `Pipe`, `Robot`, `RoundedBox`, `Component`, `Folder`, `WebBrowser`, `MobileDeviceLandscape`, `MobileDevicePortrait`

## View Modifiers

- `include *` — include all elements relevant to this view's scope
- `exclude <element>` — remove a specific element
- `autoLayout [tb|bt|lr|rl] [rankSep] [nodeSep]` — automatic layout (top-bottom default)
- `animation { ... }` — step-by-step reveal for presentations

## Groups

Visual groupings within a view:

```
model {
    bankSystem = softwareSystem "Banking" {
        group "Frontend" {
            spa = container "SPA" "" "React"
            webapp = container "Web App" "" "Spring Boot"
        }
        group "Backend" {
            api = container "API" "" "Spring Boot"
            db = container "Database" "" "PostgreSQL"
        }
    }
}
```

## Complete Example

```
workspace "Internet Banking" "An example workspace" {

    model {
        customer = person "Customer" "A bank customer"
        
        bankSystem = softwareSystem "Internet Banking System" "Allows customers to manage accounts" {
            spa = container "Single-Page App" "Banking UI" "React"
            api = container "API Application" "Banking logic" "Java/Spring Boot"
            db = container "Database" "Stores accounts, transactions" "PostgreSQL" "database"
        }
        
        mainframe = softwareSystem "Mainframe" "Core banking system" "existing"
        email = softwareSystem "E-mail System" "Sends notifications" "existing"
        
        customer -> spa "Manages accounts using"
        spa -> api "Makes API calls to" "JSON/HTTPS"
        api -> db "Reads from and writes to" "JDBC"
        api -> mainframe "Gets account data from" "XML/HTTPS"
        api -> email "Sends notifications via" "SMTP"
    }

    views {
        systemContext bankSystem "Context" {
            include *
            autoLayout
        }
        
        container bankSystem "Containers" {
            include *
            autoLayout
        }
        
        dynamic bankSystem "SignIn" "Customer sign-in flow" {
            customer -> spa "Opens banking app"
            spa -> api "Submits credentials"
            api -> db "Validates credentials"
            api -> spa "Returns session token"
        }

        styles {
            element "Person" {
                shape Person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "database" {
                shape Cylinder
            }
            element "existing" {
                background #999999
                color #ffffff
            }
        }
    }
}
```

Paste into structurizr.com/dsl to visualize.
