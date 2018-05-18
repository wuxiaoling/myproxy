VERSION 5.00
Begin VB.Form proxy 
   Caption         =   "proxy"
   ClientHeight    =   11520
   ClientLeft      =   8910
   ClientTop       =   3345
   ClientWidth     =   12135
   Icon            =   "proxy.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   768
   ScaleMode       =   3  'Pixel
   ScaleWidth      =   809
   StartUpPosition =   2  '��Ļ����
   Begin VB.CommandButton Command3 
      Caption         =   "clearText"
      Height          =   495
      Left            =   0
      TabIndex        =   10
      Top             =   3840
      Width           =   975
   End
   Begin VB.VScrollBar VScroll1 
      Height          =   11535
      Left            =   11880
      TabIndex        =   9
      Top             =   0
      Width           =   255
   End
   Begin VB.TextBox Text4 
      Height          =   11490
      Left            =   2280
      MultiLine       =   -1  'True
      TabIndex        =   8
      Text            =   "proxy.frx":4D5A
      Top             =   0
      Width           =   9600
   End
   Begin VB.TextBox Text3 
      Alignment       =   2  'Center
      Height          =   495
      Left            =   0
      ScrollBars      =   3  'Both
      TabIndex        =   7
      Text            =   "47.92.131.173"
      Top             =   2520
      Width           =   2175
   End
   Begin VB.CommandButton Command2 
      Caption         =   "reload"
      Height          =   495
      Left            =   1200
      TabIndex        =   5
      Top             =   3240
      Width           =   975
   End
   Begin VB.CommandButton Command1 
      Caption         =   "start"
      Height          =   495
      Left            =   0
      TabIndex        =   4
      Top             =   3240
      Width           =   975
   End
   Begin VB.TextBox Text2 
      Alignment       =   2  'Center
      BeginProperty DataFormat 
         Type            =   1
         Format          =   "0"
         HaveTrueFalseNull=   0
         FirstDayOfWeek  =   0
         FirstWeekOfYear =   0
         LCID            =   2052
         SubFormatType   =   1
      EndProperty
      Height          =   495
      Left            =   0
      TabIndex        =   3
      Text            =   "8099"
      Top             =   1440
      Width           =   2175
   End
   Begin VB.TextBox Text1 
      Alignment       =   2  'Center
      BeginProperty DataFormat 
         Type            =   1
         Format          =   "0"
         HaveTrueFalseNull=   0
         FirstDayOfWeek  =   0
         FirstWeekOfYear =   0
         LCID            =   2052
         SubFormatType   =   1
      EndProperty
      Height          =   495
      Left            =   0
      TabIndex        =   0
      Text            =   "80"
      Top             =   480
      Width           =   2175
   End
   Begin VB.Label Label3 
      Caption         =   "Զ��ip��ַ"
      Height          =   375
      Left            =   0
      TabIndex        =   6
      Top             =   2160
      Width           =   2175
   End
   Begin VB.Label Label2 
      Caption         =   "Զ�̶˿�"
      Height          =   375
      Left            =   0
      TabIndex        =   2
      Top             =   1080
      Width           =   2175
   End
   Begin VB.Label Label1 
      Caption         =   "���ض˿�"
      Height          =   495
      Left            =   0
      TabIndex        =   1
      Top             =   120
      Width           =   2175
   End
End
Attribute VB_Name = "proxy"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
Private ObjOldWidth As Long   '���洰���ԭʼ���
Private ObjOldHeight As Long '���洰���ԭʼ�߶�
Private ObjOldFont As Single '���洰���ԭʼ�����

'�ڵ���ResizeFormǰ�ȵ��ñ�����
Public Sub ResizeInit(FormName As Form)
   Dim Obj As Control
  
   ObjOldWidth = FormName.ScaleWidth
   ObjOldHeight = FormName.ScaleHeight
   ObjOldFont = FormName.Font.Size / ObjOldHeight
   On Error Resume Next
   For Each Obj In FormName
     Obj.Tag = Obj.Left & " " & Obj.Top & " " & Obj.Width & " " & Obj.Height & " "
   Next Obj
  
   On Error GoTo 0
End Sub

'�������ı���ڸ�Ԫ���Ĵ�С��
'�ڵ���ReSizeFormǰ�ȵ���ReSizeInit����
Public Sub ResizeForm(FormName As Form)

   Dim Pos(4) As Double
   Dim i As Long, TempPos As Long, StartPos As Long
   Dim Obj As Control
   Dim ScaleX As Double, ScaleY As Double
  
   ScaleX = FormName.ScaleWidth / ObjOldWidth
   '���洰�������ű���
   ScaleY = FormName.ScaleHeight / ObjOldHeight
   '���洰��߶����ű���
   On Error Resume Next
  
   For Each Obj In FormName
     StartPos = 1
     For i = 0 To 4
       '��ȡ�ؼ���ԭʼλ�����С
       TempPos = InStr(StartPos, Obj.Tag, " ", vbTextCompare)
       If TempPos > 0 Then
         Pos(i) = Mid(Obj.Tag, StartPos, TempPos - StartPos)
         StartPos = TempPos + 1
       Else
         Pos(i) = 0
       End If
      
       '���ݿؼ���ԭʼλ�ü�����ı��
       'С�ı����Կؼ����¶�λ��ı��С
       Obj.Move Pos(0) * ScaleX, Pos(1) * ScaleY, Pos(2) * ScaleX, Pos(3) * ScaleY
       Obj.Font.Size = ObjOldFont * FormName.ScaleHeight
     Next i
  
   Next Obj
  
   On Error GoTo 0
End Sub

Private Sub Form_Resize()
   'ȷ������ı�ʱ�ؼ���֮�ı�
   Call ResizeForm(Me)
End Sub

Private Sub Form_Load()
   '�ڳ���װ��ʱ�������
   Call ResizeInit(Me)
End Sub
