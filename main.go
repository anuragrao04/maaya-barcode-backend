package main

import (
	"fmt"
	"maaya-barcode/models"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var DB *gorm.DB

func main() {

	// connection to DB
	var err error
	DB, err = gorm.Open(sqlite.Open("test.db"), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})
	if err != nil {
		panic("failed to connect database")
	}
	DB.AutoMigrate(&models.User{})

	router := gin.Default()
	router.POST("/create", CreateUser)
	router.POST("/scan", ScanBarcode)
	router.Run(":6969")
}

type createUserRequestFormat struct {
	PRN      string `json:"prn"`
	SRN      string `json:"srn"`
	Name     string `json:"name"`
	Semester string `json:"semester"`
	Branch   string `json:"branch"`
}

func CreateUser(c *gin.Context) {
	var request createUserRequestFormat
	c.BindJSON(&request)

	newUser := models.User{
		PRN:      request.PRN,
		SRN:      request.SRN,
		Name:     request.Name,
		Semester: request.Semester,
		Branch:   request.Branch,
	}

	fmt.Println(newUser)

	result := DB.Create(&newUser)
	if result.Error != nil {
		c.JSON(400, gin.H{
			"message": "Error creating user",
		})
		return
	}
	c.JSON(200, gin.H{
		"message": "User Created Successfully",
	})
}

type scanBarcodeRequestFormat struct {
	PRN string `json:"prn"`
}

func ScanBarcode(c *gin.Context) {
	var request scanBarcodeRequestFormat
	c.BindJSON(&request)
	var user models.User
	DB.Where("prn = ?", request.PRN).First(&user)
	if user.ID == 0 {
		c.JSON(404, gin.H{
			"message": "User not found",
		})
		return
	}

	DB.Model(&user).Update("is_present", true)
	c.JSON(200, gin.H{
		"message": "User found",
		"user":    user,
	})
}
