// Generated by gencpp from file entrega1_ri/ArrayXY.msg
// DO NOT EDIT!


#ifndef ENTREGA1_RI_MESSAGE_ARRAYXY_H
#define ENTREGA1_RI_MESSAGE_ARRAYXY_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace entrega1_ri
{
template <class ContainerAllocator>
struct ArrayXY_
{
  typedef ArrayXY_<ContainerAllocator> Type;

  ArrayXY_()
    : x()
    , y()  {
    }
  ArrayXY_(const ContainerAllocator& _alloc)
    : x(_alloc)
    , y(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> _x_type;
  _x_type x;

   typedef std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> _y_type;
  _y_type y;





  typedef boost::shared_ptr< ::entrega1_ri::ArrayXY_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::entrega1_ri::ArrayXY_<ContainerAllocator> const> ConstPtr;

}; // struct ArrayXY_

typedef ::entrega1_ri::ArrayXY_<std::allocator<void> > ArrayXY;

typedef boost::shared_ptr< ::entrega1_ri::ArrayXY > ArrayXYPtr;
typedef boost::shared_ptr< ::entrega1_ri::ArrayXY const> ArrayXYConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::entrega1_ri::ArrayXY_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::entrega1_ri::ArrayXY_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::entrega1_ri::ArrayXY_<ContainerAllocator1> & lhs, const ::entrega1_ri::ArrayXY_<ContainerAllocator2> & rhs)
{
  return lhs.x == rhs.x &&
    lhs.y == rhs.y;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::entrega1_ri::ArrayXY_<ContainerAllocator1> & lhs, const ::entrega1_ri::ArrayXY_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace entrega1_ri

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::entrega1_ri::ArrayXY_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::entrega1_ri::ArrayXY_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::entrega1_ri::ArrayXY_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::entrega1_ri::ArrayXY_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::entrega1_ri::ArrayXY_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::entrega1_ri::ArrayXY_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::entrega1_ri::ArrayXY_<ContainerAllocator> >
{
  static const char* value()
  {
    return "796182af49bd48aa8ba60ed21519725c";
  }

  static const char* value(const ::entrega1_ri::ArrayXY_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x796182af49bd48aaULL;
  static const uint64_t static_value2 = 0x8ba60ed21519725cULL;
};

template<class ContainerAllocator>
struct DataType< ::entrega1_ri::ArrayXY_<ContainerAllocator> >
{
  static const char* value()
  {
    return "entrega1_ri/ArrayXY";
  }

  static const char* value(const ::entrega1_ri::ArrayXY_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::entrega1_ri::ArrayXY_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64[] x\n"
"float64[] y\n"
;
  }

  static const char* value(const ::entrega1_ri::ArrayXY_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::entrega1_ri::ArrayXY_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.x);
      stream.next(m.y);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ArrayXY_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::entrega1_ri::ArrayXY_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::entrega1_ri::ArrayXY_<ContainerAllocator>& v)
  {
    s << indent << "x[]" << std::endl;
    for (size_t i = 0; i < v.x.size(); ++i)
    {
      s << indent << "  x[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.x[i]);
    }
    s << indent << "y[]" << std::endl;
    for (size_t i = 0; i < v.y.size(); ++i)
    {
      s << indent << "  y[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.y[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // ENTREGA1_RI_MESSAGE_ARRAYXY_H
